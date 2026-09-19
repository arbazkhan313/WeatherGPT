from fastapi import APIRouter, HTTPException, Query

from app.services.weather_service import WeatherService
from app.services.location_service import LocationService


router = APIRouter(
    prefix="/weather",
    tags=["Weather"]
)

weather_service = WeatherService()
location_service = LocationService()


@router.get("/current")
async def get_current_weather(
    latitude: float = Query(..., description="Latitude of the location"),
    longitude: float = Query(..., description="Longitude of the location")
):
    try:
        weather = await weather_service.get_current_weather(
            latitude,
            longitude
        )

        return {
            "success": True,
            "data": weather
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/city")
async def get_weather_by_city(
    city: str = Query(..., description="City or place name")
):
    try:
        locations = await location_service.search_location(city)

        if not locations:
            raise HTTPException(
                status_code=404,
                detail="Location not found"
            )

        location = locations[0]

        weather = await weather_service.get_current_weather(
            location["latitude"],
            location["longitude"]
        )

        return {
            "success": True,
            "location": location,
            "weather": weather
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
