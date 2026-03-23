from fastapi import APIRouter
from services.data_source_manager import data_source_manager
import os

router = APIRouter()

@router.get("/status")
async def get_system_status():
    """Get system status and data source information"""
    return {
        "status": "operational",
        "data_sources": {
            "mode": "mock" if data_source_manager.use_mock_data else "live",
            "opensky": {
                "available": data_source_manager.opensky_available,
                "status": "connected" if data_source_manager.opensky_available else "using_mock"
            },
            "nasa_firms": {
                "available": data_source_manager.nasa_available,
                "status": "connected" if data_source_manager.nasa_available else "using_mock"
            }
        },
        "environment": {
            "use_mock_data": os.getenv("USE_MOCK_DATA", "false"),
            "nasa_api_configured": bool(os.getenv("NASA_FIRMS_API_KEY") and os.getenv("NASA_FIRMS_API_KEY") != "your_api_key_here")
        }
    }

@router.post("/toggle-mock")
async def toggle_mock_mode():
    """Toggle between mock and live data (for development)"""
    data_source_manager.use_mock_data = not data_source_manager.use_mock_data
    return {
        "mode": "mock" if data_source_manager.use_mock_data else "live",
        "message": f"Switched to {'mock' if data_source_manager.use_mock_data else 'live'} data mode"
    }
