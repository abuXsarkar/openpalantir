from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database_lite import async_session_maker, AircraftPosition

router = APIRouter()

async def get_session():
    async with async_session_maker() as session:
        yield session

@router.get("/positions")
async def get_aircraft_positions(session: AsyncSession = Depends(get_session)):
    """Get all current aircraft positions as GeoJSON"""
    result = await session.execute(select(AircraftPosition))
    
    features = []
    for row in result.scalars():
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row.longitude, row.latitude]
            },
            "properties": {
                "icao24": row.icao24,
                "callsign": row.callsign,
                "country": row.origin_country,
                "altitude": row.altitude,
                "velocity": row.velocity,
                "heading": row.heading,
                "type": "aircraft"
            }
        })
    
    return {
        "type": "FeatureCollection",
        "features": features
    }
