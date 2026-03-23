from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import async_session_maker, ThermalAnomaly

router = APIRouter()

async def get_session():
    async with async_session_maker() as session:
        yield session

@router.get("/anomalies")
async def get_thermal_anomalies(session: AsyncSession = Depends(get_session)):
    """Get thermal anomalies from NASA FIRMS"""
    result = await session.execute(select(ThermalAnomaly))
    anomalies = result.scalars().all()
    
    features = []
    for anomaly in anomalies:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [anomaly.longitude, anomaly.latitude]
            },
            "properties": {
                "brightness": anomaly.brightness,
                "confidence": anomaly.confidence,
                "satellite": anomaly.satellite,
                "scan_time": anomaly.scan_time.isoformat() if anomaly.scan_time else None,
                "type": "thermal"
            }
        })
    
    return {
        "type": "FeatureCollection",
        "features": features
    }
