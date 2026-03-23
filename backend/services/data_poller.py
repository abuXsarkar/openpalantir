import asyncio
import httpx
from datetime import datetime
from sqlalchemy import select, delete
from database import async_session_maker, AircraftPosition, ThermalAnomaly
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

class DataPoller:
    def __init__(self):
        self.running = False
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def start_polling(self):
        self.running = True
        await asyncio.gather(
            self.poll_aviation(),
            self.poll_thermal()
        )
    
    async def stop_polling(self):
        self.running = False
        await self.client.aclose()
    
    async def poll_aviation(self):
        """Poll OpenSky Network for aircraft positions"""
        while self.running:
            try:
                # Focus on Middle East region
                response = await self.client.get(
                    "https://opensky-network.org/api/states/all",
                    params={"lamin": 12, "lomin": 25, "lamax": 42, "lomax": 63}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    async with async_session_maker() as session:
                        await session.execute(delete(AircraftPosition))
                        
                        if data.get("states"):
                            for state in data["states"]:
                                if state[5] and state[6]:  # Has lat/lon
                                    aircraft = AircraftPosition(
                                        icao24=state[0],
                                        callsign=state[1].strip() if state[1] else None,
                                        origin_country=state[2],
                                        time_position=state[3],
                                        last_contact=state[4],
                                        longitude=state[5],
                                        latitude=state[6],
                                        altitude=state[7],
                                        velocity=state[9],
                                        heading=state[10],
                                        geom=from_shape(Point(state[5], state[6]), srid=4326)
                                    )
                                    session.add(aircraft)
                        
                        await session.commit()
                        print(f"Updated {len(data.get('states', []))} aircraft positions")
            
            except Exception as e:
                print(f"Aviation polling error: {e}")
            
            await asyncio.sleep(30)  # Poll every 30 seconds
    
    async def poll_thermal(self):
        """Poll NASA FIRMS for thermal anomalies"""
        while self.running:
            try:
                # VIIRS data for last 24h (requires API key - using demo endpoint)
                response = await self.client.get(
                    "https://firms.modaps.eosdis.nasa.gov/api/area/csv/[YOUR_API_KEY]/VIIRS_NOAA20_NRT/world/1"
                )
                
                # For MVP, simulate thermal data
                print("Thermal polling (requires NASA FIRMS API key)")
            
            except Exception as e:
                print(f"Thermal polling error: {e}")
            
            await asyncio.sleep(300)  # Poll every 5 minutes
