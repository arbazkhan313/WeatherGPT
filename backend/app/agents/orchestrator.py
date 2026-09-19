import re
from datetime import date, timedelta

from app.services.location_service import LocationService
from app.services.weather_service import WeatherService
from app.services.forecast_service import ForecastService
from app.services.historical_weather_service import HistoricalWeatherService
from app.services.llm_service import LLMService


class WeatherOrchestrator:

    def __init__(self):
        self.name = "WeatherGPT Orchestrator"

        self.location_service = LocationService()
        self.weather_service = WeatherService()
        self.forecast_service = ForecastService()
        self.historical_weather_service = HistoricalWeatherService()
        self.llm_service = LLMService()

    def extract_city(self, user_query: str):

        query = user_query.strip()

        patterns = [
            r"weather\s+(?:in|at|for)\s+([a-zA-Z\s]+)",
            r"temperature\s+(?:in|at|for)\s+([a-zA-Z\s]+)",
            r"forecast\s+(?:in|at|for)\s+([a-zA-Z\s]+)",
            r"rain(?:ing)?\s+(?:in|at|for)\s+([a-zA-Z\s]+)",
            r"umbrella\s+(?:in|at|for)\s+([a-zA-Z\s]+)",
            r"storm\s+(?:in|at|for)\s+([a-zA-Z\s]+)",
            r"cyclone\s+(?:in|at|for)\s+([a-zA-Z\s]+)",
            r"flood\s+(?:in|at|for)\s+([a-zA-Z\s]+)",
            r"heatwave\s+(?:in|at|for)\s+([a-zA-Z\s]+)",
            r"tomorrow\s+(?:in|at|for)\s+([a-zA-Z\s]+)",
            r"history\s+(?:of|in|for)\s+([a-zA-Z\s]+)",
            r"historical\s+(?:weather\s+)?(?:of|in|for)\s+([a-zA-Z\s]+)",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                query,
                re.IGNORECASE
            )

            if match:

                city = match.group(1).strip()

                city = re.sub(
                    r"\s+(today|tomorrow|tonight|last year|previous year)$",
                    "",
                    city,
                    flags=re.IGNORECASE
                )

                return city.rstrip("?.!,").strip()

        patterns_with_city_before_time = [
            r"(?:go to|visit|travel to|going to)\s+([a-zA-Z\s]+?)\s+(?:today|tomorrow|tonight)",
            r"(?:rain|raining|hot|cold)\s+(?:in|at)\s+([a-zA-Z\s]+?)\s+(?:today|tomorrow|tonight)",
            r"(?:weather)\s+(?:like)\s+(?:in|at)\s+([a-zA-Z\s]+?)\s+(?:last year|previous year)",
        ]

        for pattern in patterns_with_city_before_time:

            match = re.search(
                pattern,
                query,
                re.IGNORECASE
            )

            if match:

                city = match.group(1).strip()

                return city.rstrip("?.!,").strip()

        return None

    def detect_intent(self, user_query: str):

        query = user_query.lower()

        # Historical intent
        if any(word in query for word in [
            "historical",
            "history",
            "last year",
            "previous year",
            "past weather",
            "historically",
            "recorded weather",
            "weather history"
        ]):
            return "historical"

        # Forecast intent
        if any(word in query for word in [
            "forecast",
            "tomorrow",
            "tonight",
            "next week",
            "next few days",
            "coming days",
            "later today",
            "will it be",
            "going to rain",
            "going to be"
        ]):
            return "forecast"

        # Rain intent
        if any(word in query for word in [
            "rain",
            "raining",
            "precipitation",
            "umbrella",
            "drizzle"
        ]):
            return "rain"

        # Risk intent
        if any(word in query for word in [
            "storm",
            "cyclone",
            "flood",
            "heatwave",
            "severe weather",
            "warning",
            "danger",
            "unsafe",
            "risk"
        ]):
            return "risk"

        # Temperature intent
        if any(word in query for word in [
            "temperature",
            "hot",
            "cold",
            "heat",
            "cool"
        ]):
            return "temperature"

        return "current"

    async def process(self, user_query: str):

        city = self.extract_city(user_query)

        intent = self.detect_intent(user_query)

        if not city:
            return {
                "success": False,
                "intent": intent,
                "message": "I could not identify the city from your question."
            }

        locations = await self.location_service.search_location(city)

        if not locations:
            return {
                "success": False,
                "city": city,
                "intent": intent,
                "message": "Location not found."
            }

        location = locations[0]

        # --------------------------------
        # HISTORICAL WEATHER
        # --------------------------------

        if intent == "historical":

            today = date.today()

            start_date = date(
                today.year - 1,
                1,
                1
            )

            end_date = date(
                today.year - 1,
                12,
                31
            )

            historical_data = await self.historical_weather_service.get_historical_weather(
                location["latitude"],
                location["longitude"],
                start_date.isoformat(),
                end_date.isoformat()
            )

            hourly = historical_data["hourly"]

            temperatures = [
                value
                for value in hourly["temperature_2m"]
                if value is not None
            ]

            precipitation = [
                value
                for value in hourly["precipitation"]
                if value is not None
            ]

            humidity = [
                value
                for value in hourly["relative_humidity_2m"]
                if value is not None
            ]

            wind_speed = [
                value
                for value in hourly["wind_speed_10m"]
                if value is not None
            ]

            summary = {
                "year": today.year - 1,
                "average_temperature": (
                    round(sum(temperatures) / len(temperatures), 2)
                    if temperatures else None
                ),
                "maximum_temperature": (
                    max(temperatures)
                    if temperatures else None
                ),
                "minimum_temperature": (
                    min(temperatures)
                    if temperatures else None
                ),
                "total_precipitation_mm": (
                    round(sum(precipitation), 2)
                    if precipitation else None
                ),
                "average_humidity": (
                    round(sum(humidity) / len(humidity), 2)
                    if humidity else None
                ),
                "maximum_wind_speed_kmh": (
                    max(wind_speed)
                    if wind_speed else None
                )
            }

            prompt = f"""
You are WeatherGPT.

User question:
{user_query}

Detected intent:
historical weather

Location:
{location["name"]}, {location.get("state")}, {location["country"]}

Historical weather summary for {today.year - 1}:

Average temperature:
{summary["average_temperature"]}°C

Maximum temperature:
{summary["maximum_temperature"]}°C

Minimum temperature:
{summary["minimum_temperature"]}°C

Total precipitation:
{summary["total_precipitation_mm"]} mm

Average humidity:
{summary["average_humidity"]}%

Maximum wind speed:
{summary["maximum_wind_speed_kmh"]} km/h

Answer the user's question using ONLY the historical information provided.

Explain the result clearly and practically.

Do not invent information.
"""

            answer = await self.llm_service.generate_response(prompt)

            return {
                "success": True,
                "query": user_query,
                "intent": intent,
                "location": location,
                "historical_period": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat()
                },
                "summary": summary,
                "answer": answer
            }

        # --------------------------------
        # FORECAST
        # --------------------------------

        if intent == "forecast":

            forecast_data = await self.forecast_service.get_forecast(
                location["latitude"],
                location["longitude"]
            )

            forecast_text = "\n".join(
                [
                    f'{item["datetime"]}: '
                    f'{item["temperature"]}°C, '
                    f'{item["weather"]}'
                    for item in forecast_data["forecast"][:8]
                ]
            )

            prompt = f"""
You are WeatherGPT.

User question:
{user_query}

Detected intent:
forecast

Location:
{location["name"]}, {location.get("state")}, {location["country"]}

Upcoming forecast:
{forecast_text}

Answer the user's question using ONLY the forecast information provided.

Give a practical and easy-to-understand answer.

If the user asks whether they should carry an umbrella,
use the available rain/weather information to answer.

Do not invent weather information.
"""

            answer = await self.llm_service.generate_response(prompt)

            return {
                "success": True,
                "query": user_query,
                "intent": intent,
                "location": location,
                "forecast": forecast_data,
                "answer": answer
            }

        # --------------------------------
        # CURRENT WEATHER
        # --------------------------------

        weather = await self.weather_service.get_current_weather(
            location["latitude"],
            location["longitude"]
        )

        prompt = f"""
You are WeatherGPT.

User question:
{user_query}

Detected intent:
{intent}

Location:
{location["name"]}, {location.get("state")}, {location["country"]}

Current weather:
Temperature: {weather["temperature"]}°C
Feels like: {weather["feels_like"]}°C
Humidity: {weather["humidity"]}%
Pressure: {weather["pressure"]} hPa
Wind speed: {weather["wind_speed"]} m/s
Condition: {weather["weather"]}

Answer the user's question using ONLY the weather information provided.

Be clear, concise and practical.

Do not invent weather information.
"""

        answer = await self.llm_service.generate_response(prompt)

        return {
            "success": True,
            "query": user_query,
            "intent": intent,
            "location": location,
            "weather": weather,
            "answer": answer
        }
