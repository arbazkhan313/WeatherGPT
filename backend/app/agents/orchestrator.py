import re
from datetime import date

from app.services.location_service import LocationService
from app.services.weather_service import WeatherService
from app.services.forecast_service import ForecastService
from app.services.historical_weather_service import HistoricalWeatherService
from app.services.llm_service import LLMService
from app.agents.risk_agent import RiskAgent


class WeatherOrchestrator:

    def __init__(self):
        self.name = "WeatherGPT Orchestrator"

        self.location_service = LocationService()
        self.weather_service = WeatherService()
        self.forecast_service = ForecastService()
        self.historical_weather_service = HistoricalWeatherService()
        self.llm_service = LLMService()
        self.risk_agent = RiskAgent()

    # =========================================================
    # CITY EXTRACTION
    # =========================================================

    def extract_city(self, user_query: str):

        query = user_query.strip()

        # -----------------------------------------------------
        # Questions where the city comes after the weather term
        # -----------------------------------------------------

        patterns = [

            # Current weather
            r"weather\s+(?:in|at|for)\s+([a-zA-Z\s]+)",

            r"temperature\s+(?:in|at|for)\s+([a-zA-Z\s]+)",

            r"how\s+does\s+the\s+temperature\s+feel\s+(?:in|at|for)\s+([a-zA-Z\s]+)",

            r"how\s+does\s+it\s+feel\s+(?:in|at|for)\s+([a-zA-Z\s]+)",

            r"what\s+does\s+the\s+temperature\s+feel\s+like\s+(?:in|at|for)\s+([a-zA-Z\s]+)",

            r"what\s+does\s+it\s+feel\s+like\s+(?:in|at|for)\s+([a-zA-Z\s]+)",

            # Forecast
            r"forecast\s+(?:in|at|for)\s+([a-zA-Z\s]+)",

            r"prediction\s+(?:in|at|for)\s+([a-zA-Z\s]+)",

            # Rain
            r"rain(?:ing)?\s+(?:in|at|for)\s+([a-zA-Z\s]+)",

            r"umbrella\s+(?:in|at|for)\s+([a-zA-Z\s]+)",

            r"precipitation\s+(?:in|at|for)\s+([a-zA-Z\s]+)",

            # Severe weather
            r"storm\s+(?:in|at|for)\s+([a-zA-Z\s]+)",

            r"cyclone\s+(?:in|at|for)\s+([a-zA-Z\s]+)",

            r"flood\s+(?:in|at|for)\s+([a-zA-Z\s]+)",

            r"flooding\s+(?:in|at|for)\s+([a-zA-Z\s]+)",

            r"heatwave\s+(?:in|at|for)\s+([a-zA-Z\s]+)",

            r"danger\s+(?:in|at|for)\s+([a-zA-Z\s]+)",

            r"risk\s+(?:in|at|for)\s+([a-zA-Z\s]+)",

            r"warning\s+(?:in|at|for)\s+([a-zA-Z\s]+)",

            # Historical
            r"history\s+(?:of|in|for)\s+([a-zA-Z\s]+)",

            r"historical\s+(?:weather\s+)?(?:of|in|for)\s+([a-zA-Z\s]+)",

            r"past\s+weather\s+(?:in|at|for)\s+([a-zA-Z\s]+)",
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
                    r"\s+(today|tomorrow|tonight|yesterday|last year|previous year)$",
                    "",
                    city,
                    flags=re.IGNORECASE
                )

                return city.rstrip("?.!,").strip()

        # -----------------------------------------------------
        # Questions where city comes BEFORE time
        # -----------------------------------------------------

        patterns_with_city_before_time = [

            r"(?:go to|visit|travel to|going to)\s+([a-zA-Z\s]+?)\s+(?:today|tomorrow|tonight)",

            r"(?:rain|raining|hot|cold|cool|warm)\s+(?:in|at)\s+([a-zA-Z\s]+?)\s+(?:today|tomorrow|tonight)",

            r"(?:weather)\s+(?:like)\s+(?:in|at)\s+([a-zA-Z\s]+?)\s+(?:last year|previous year)",

            r"(?:danger|risk|flooding|flood|storm|cyclone|heatwave)\s+(?:in|at|for)\s+([a-zA-Z\s]+?)\s+(?:today|tomorrow|tonight)",

            # Example:
            # Is Mandya hot today?
            r"(?:is|will)\s+([a-zA-Z\s]+?)\s+(?:hot|cold|rainy|raining|windy|stormy)\s+(?:today|tomorrow|tonight)",

            # Example:
            # Is it raining in Mandya today?
            r"(?:is|will)\s+(?:it|the weather)\s+(?:be\s+)?(?:rainy|raining|hot|cold|windy)\s+(?:in|at)\s+([a-zA-Z\s]+)",

            # Example:
            # Can I travel to Mandya tomorrow?
            r"(?:travel|go|visit|drive)\s+(?:to)\s+([a-zA-Z\s]+?)\s+(?:today|tomorrow|tonight)",
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

        # -----------------------------------------------------
        # Direct city extraction for common natural questions
        # -----------------------------------------------------

        natural_patterns = [

            # How is Mandya today?
            r"how\s+is\s+([a-zA-Z\s]+?)\s+(?:today|tomorrow|tonight)",

            # How's Mandya today?
            r"how'?s\s+([a-zA-Z\s]+?)\s+(?:today|tomorrow|tonight)",

            # Is Mandya safe today?
            r"is\s+([a-zA-Z\s]+?)\s+safe\s+(?:today|tomorrow|tonight)",

            # What should I wear in Mandya?
            r"what\s+should\s+i\s+(?:wear|take|carry)\s+(?:in|at)\s+([a-zA-Z\s]+)",

            # Can I go outside in Mandya?
            r"(?:can|should)\s+i\s+(?:go\s+outside|go\s+out)\s+(?:in|at)\s+([a-zA-Z\s]+)",

            # Is it safe to travel in Mandya?
            r"is\s+it\s+safe\s+to\s+(?:travel|go|drive)\s+(?:in|to)\s+([a-zA-Z\s]+)",
        ]

        for pattern in natural_patterns:

            match = re.search(
                pattern,
                query,
                re.IGNORECASE
            )

            if match:

                city = match.group(1).strip()

                return city.rstrip("?.!,").strip()

        return None

    # =========================================================
    # INTENT DETECTION
    # =========================================================

    def detect_intent(self, user_query: str):

        query = user_query.lower()

        # -----------------------------------------------------
        # Risk intent
        # -----------------------------------------------------

        if any(word in query for word in [
            "danger",
            "risk",
            "unsafe",
            "warning",
            "severe weather",
            "storm",
            "cyclone",
            "flood",
            "flooding",
            "heatwave",
            "heavy rain",
            "extreme weather",
            "safe to travel",
            "safe to go",
            "weather risk"
        ]):

            return "risk"

        # -----------------------------------------------------
        # Historical intent
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Forecast intent
        # -----------------------------------------------------

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
            "going to be",
            "expected",
            "upcoming"
        ]):

            return "forecast"

        # -----------------------------------------------------
        # Rain intent
        # -----------------------------------------------------

        if any(word in query for word in [
            "rain",
            "raining",
            "precipitation",
            "umbrella",
            "drizzle"
        ]):

            return "rain"

        # -----------------------------------------------------
        # Temperature intent
        # -----------------------------------------------------

        if any(word in query for word in [
            "temperature",
            "hot",
            "cold",
            "heat",
            "cool",
            "warm",
            "feel like",
            "feels like"
        ]):

            return "temperature"

        # -----------------------------------------------------
        # Default
        # -----------------------------------------------------

        return "current"

    # =========================================================
    # MAIN AGENT PROCESS
    # =========================================================

    async def process(self, user_query: str):

        city = self.extract_city(user_query)

        intent = self.detect_intent(user_query)

        # -----------------------------------------------------
        # City not detected
        # -----------------------------------------------------

        if not city:

            return {
                "success": False,
                "intent": intent,
                "message": "I could not identify the city from your question."
            }

        # -----------------------------------------------------
        # Search location
        # -----------------------------------------------------

        locations = await self.location_service.search_location(city)

        if not locations:

            return {
                "success": False,
                "city": city,
                "intent": intent,
                "message": "Location not found."
            }

        location = locations[0]

        # =====================================================
        # RISK INTENT
        # =====================================================

        if intent == "risk":

            current_weather = await self.weather_service.get_current_weather(
                location["latitude"],
                location["longitude"]
            )

            forecast_data = await self.forecast_service.get_forecast(
                location["latitude"],
                location["longitude"]
            )

            risk_result = self.risk_agent.analyze_risk(
                current_weather,
                forecast_data
            )

            risk_text = ""

            for risk in risk_result["risks"]:

                risk_text += f"""
Risk Type: {risk["type"]}
Risk Level: {risk["level"]}
Reason: {risk["reason"]}
Safety Advice: {risk["advice"]}
"""

            if not risk_text:

                risk_text = (
                    "No significant weather risk indicators were detected."
                )

            prompt = f"""
You are WeatherGPT, an intelligent weather risk assistant.

User question:
{user_query}

Location:
{location["name"]}, {location.get("state")}, {location["country"]}

Current Weather:
Temperature: {current_weather["temperature"]}°C
Feels like: {current_weather["feels_like"]}°C
Humidity: {current_weather["humidity"]}%
Wind speed: {current_weather["wind_speed"]} m/s
Condition: {current_weather["weather"]}

Risk Analysis:

Overall Risk Level:
{risk_result["overall_level"]}

Detected Risks:
{risk_text}

Your task:

1. Clearly answer the user's question.
2. Explain the detected weather risks.
3. Mention the overall risk level.
4. Give practical safety advice.
5. Use ONLY the weather and risk information provided above.
6. Do NOT invent warnings, rainfall amounts, flooding events,
   government alerts, emergency situations, or other weather facts.
7. Do NOT claim that flooding is occurring unless the provided
   data explicitly indicates it.
8. If there is insufficient information to confirm a specific danger,
   clearly say that the available data does not confirm it.

Keep the answer concise and practical.
"""

            answer = await self.llm_service.generate_response(prompt)

            return {
                "success": True,
                "query": user_query,
                "intent": intent,
                "location": location,
                "current_weather": current_weather,
                "risk_analysis": risk_result,
                "answer": answer
            }

        # =====================================================
        # HISTORICAL INTENT
        # =====================================================

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

            historical_data = (
                await self.historical_weather_service.get_historical_weather(
                    location["latitude"],
                    location["longitude"],
                    start_date.isoformat(),
                    end_date.isoformat()
                )
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
                    round(
                        sum(temperatures) / len(temperatures),
                        2
                    )
                    if temperatures
                    else None
                ),

                "maximum_temperature": (
                    max(temperatures)
                    if temperatures
                    else None
                ),

                "minimum_temperature": (
                    min(temperatures)
                    if temperatures
                    else None
                ),

                "total_precipitation_mm": (
                    round(
                        sum(precipitation),
                        2
                    )
                    if precipitation
                    else None
                ),

                "average_humidity": (
                    round(
                        sum(humidity) / len(humidity),
                        2
                    )
                    if humidity
                    else None
                ),

                "maximum_wind_speed_kmh": (
                    max(wind_speed)
                    if wind_speed
                    else None
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

You may interpret the numbers, but do not add unsupported facts.

Do not claim anything about:
- water availability
- climate classification
- agricultural conditions
- drought
- flooding
- local climate trends

unless that information is explicitly present above.

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

        # =====================================================
        # FORECAST INTENT
        # =====================================================

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

        # =====================================================
        # CURRENT / TEMPERATURE / RAIN INTENT
        # =====================================================

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

If the user asks how the temperature feels,
use the "feels like" temperature.

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
