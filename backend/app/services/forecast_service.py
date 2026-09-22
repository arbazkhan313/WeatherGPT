import os
import httpx

from dotenv import load_dotenv

load_dotenv()


class ForecastService:

    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/forecast"

    async def get_forecast(
        self,
        latitude: float,
        longitude: float
    ):

        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY is not configured")

        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": self.api_key,
            "units": "metric"
        }

        async with httpx.AsyncClient() as client:

            response = await client.get(
                self.base_url,
                params=params,
                timeout=10.0
            )

        response.raise_for_status()

        data = response.json()

        forecast = []

        for item in data["list"]:

            # -----------------------------------------
            # RAIN AMOUNT
            # -----------------------------------------

            rain_data = item.get("rain", {})

            rain_3h = rain_data.get("3h", 0)

            # -----------------------------------------
            # SNOW AMOUNT
            # -----------------------------------------

            snow_data = item.get("snow", {})

            snow_3h = snow_data.get("3h", 0)

            # -----------------------------------------
            # PRECIPITATION PROBABILITY
            # -----------------------------------------

            precipitation_probability = item.get("pop", 0) * 100

            # -----------------------------------------
            # WEATHER
            # -----------------------------------------

            weather_main = item["weather"][0]["main"]
            weather_description = item["weather"][0]["description"]

            # -----------------------------------------
            # CLOUD COVER
            # -----------------------------------------

            cloud_cover = item.get("clouds", {}).get("all", 0)

            # -----------------------------------------
            # FORECAST OBJECT
            # -----------------------------------------

            forecast.append({

                "datetime": item["dt_txt"],

                "temperature": item["main"]["temp"],

                "feels_like": item["main"]["feels_like"],

                "humidity": item["main"]["humidity"],

                "pressure": item["main"]["pressure"],

                "weather": weather_description,

                "weather_main": weather_main,

                "wind_speed": item["wind"]["speed"],

                "wind_gust": item.get("wind", {}).get("gust", 0),

                "precipitation_probability": round(
                    precipitation_probability,
                    1
                ),

                "rain_3h_mm": rain_3h,

                "snow_3h_mm": snow_3h,

                "cloud_cover": cloud_cover
            })

        return {
            "location": data["city"]["name"],
            "country": data["city"]["country"],
            "forecast": forecast
        }
