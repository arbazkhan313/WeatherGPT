import httpx


class HistoricalWeatherService:

    def __init__(self):
        self.base_url = "https://archive-api.open-meteo.com/v1/archive"

    async def get_historical_weather(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str
    ):

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "precipitation,"
                "wind_speed_10m"
            ),
            "timezone": "auto",
            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh",
            "precipitation_unit": "mm"
        }

        async with httpx.AsyncClient() as client:

            response = await client.get(
                self.base_url,
                params=params,
                timeout=20.0
            )

        response.raise_for_status()

        data = response.json()

        return {
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "timezone": data["timezone"],
            "hourly": data["hourly"]
        }
