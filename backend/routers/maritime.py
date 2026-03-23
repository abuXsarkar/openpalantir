from fastapi import APIRouter

router = APIRouter()

@router.get("/vessels")
async def get_vessels():
    """Get maritime vessel positions (placeholder for AIS integration)"""
    return {
        "type": "FeatureCollection",
        "features": []
    }
