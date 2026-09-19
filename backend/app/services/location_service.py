import os
import httpx
from dotenv import load_dotenv

load_dotenv()


class LocationService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/geo/1.0/direct"

    async def search_location(self, city: str):
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY is not configured")

        params = {
            "q": city,
            "limit": 5,
            "appid": self.api_key
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.base_url,
                params=params,
                timeout=10.0
            )

        response.raise_for_status()

        data = response.json()

        locations = []

        for item in data:
            locations.append({
                "name": item.get("name"),
                "state": item.get("state"),
                "country": item.get("country"),
                "latitude": item.get("lat"),
                "longitude": item.get("lon")
            })

        return locations
