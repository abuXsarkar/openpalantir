from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import async_session_maker, GeopoliticalEvent

router = APIRouter()

async def get_session():
    async with async_session_maker() as session:
        yield session

@router.get("/geopolitical")
async def get_geopolitical_events(session: AsyncSession = Depends(get_session)):
    """Get geopolitical events from GDELT"""
    result = await session.execute(select(GeopoliticalEvent))
    events = result.scalars().all()
    
    features = []
    for event in events:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [event.longitude, event.latitude]
            },
            "properties": {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "actor1": event.actor1,
                "actor2": event.actor2,
                "goldstein_scale": event.goldstein_scale,
                "source_url": event.source_url,
                "type": "event"
            }
        })
    
    return {
        "type": "FeatureCollection",
        "features": features
    }
