from fastapi import APIRouter, HTTPException, Query

from app.services.location_service import LocationService
from app.services.forecast_service import ForecastService


router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"]
)

location_service = LocationService()
forecast_service = ForecastService()


@router.get("/city")
async def get_forecast_by_city(
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

        forecast = await forecast_service.get_forecast(
            location["latitude"],
            location["longitude"]
        )

        return {
            "success": True,
            "location": location,
            "forecast": forecast
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
