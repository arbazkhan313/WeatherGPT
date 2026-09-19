import os
import httpx
from dotenv import load_dotenv

load_dotenv()


class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    async def get_current_weather(self, latitude: float, longitude: float):
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

        return {
            "location": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "weather": data["weather"][0]["description"],
            "weather_main": data["weather"][0]["main"],
        }
