import os
import httpx
from dotenv import load_dotenv

load_dotenv()


class ForecastService:

    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/forecast"

    async def get_forecast(self, latitude: float, longitude: float):

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
            forecast.append({
                "datetime": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "feels_like": item["main"]["feels_like"],
                "humidity": item["main"]["humidity"],
                "weather": item["weather"][0]["description"],
                "weather_main": item["weather"][0]["main"],
                "wind_speed": item["wind"]["speed"]
            })

        return {
            "location": data["city"]["name"],
            "country": data["city"]["country"],
            "forecast": forecast
        }
