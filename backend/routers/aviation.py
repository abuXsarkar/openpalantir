from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database import async_session_maker, AircraftPosition
from geoalchemy2.functions import ST_AsGeoJSON

router = APIRouter()

async def get_session():
    async with async_session_maker() as session:
        yield session

@router.get("/positions")
async def get_aircraft_positions(session: AsyncSession = Depends(get_session)):
    """Get all current aircraft positions as GeoJSON"""
    result = await session.execute(
        select(
            AircraftPosition.icao24,
            AircraftPosition.callsign,
            AircraftPosition.origin_country,
            AircraftPosition.altitude,
            AircraftPosition.velocity,
            AircraftPosition.heading,
            AircraftPosition.longitude,
            AircraftPosition.latitude
        )
    )
    
    features = []
    for row in result:
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
