from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session_maker
from services.alert_system import AlertSystem

router = APIRouter()
alert_system = AlertSystem()

async def get_session():
    async with async_session_maker() as session:
        yield session

@router.get("/current")
async def get_current_alerts(session: AsyncSession = Depends(get_session)):
    """Get all current intelligence alerts"""
    alerts = await alert_system.get_all_alerts(session)
    return {
        "count": len(alerts),
        "alerts": alerts
    }

@router.get("/thermal")
async def get_thermal_alerts(session: AsyncSession = Depends(get_session)):
    """Get thermal proximity alerts only"""
    alerts = await alert_system.check_thermal_proximity(session)
    return {
        "count": len(alerts),
        "alerts": alerts
    }

@router.get("/aircraft")
async def get_aircraft_alerts(session: AsyncSession = Depends(get_session)):
    """Get military aircraft alerts only"""
    alerts = await alert_system.check_aircraft_proximity(session)
    return {
        "count": len(alerts),
        "alerts": alerts
    }

@router.get("/locations")
async def get_sensitive_locations():
    """Get list of monitored sensitive locations"""
    from services.alert_system import SENSITIVE_LOCATIONS
    
    features = []
    for loc in SENSITIVE_LOCATIONS:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [loc['lon'], loc['lat']]
            },
            "properties": {
                "name": loc['name'],
                "country": loc['country'],
                "type": loc['type']
            }
        })
    
    return {
        "type": "FeatureCollection",
        "features": features
    }
