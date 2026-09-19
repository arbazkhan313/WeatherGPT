from fastapi import APIRouter, HTTPException, Query

from app.services.location_service import LocationService

router = APIRouter(
    prefix="/location",
    tags=["Location"]
)

location_service = LocationService()


@router.get("/search")
async def search_location(
    city: str = Query(..., description="City or place name")
):
    try:
        locations = await location_service.search_location(city)

        return {
            "success": True,
            "data": locations
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
