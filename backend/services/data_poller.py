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
        import os
        from datetime import datetime, timedelta
        
        api_key = os.getenv("NASA_FIRMS_API_KEY")
        
        while self.running:
            try:
                if not api_key or api_key == "your_api_key_here":
                    print("NASA FIRMS API key not configured, skipping thermal polling")
                    await asyncio.sleep(300)
                    continue
                
                # Focus on Middle East and conflict zones
                regions = [
                    {"name": "Middle_East", "lamin": 12, "lomin": 25, "lamax": 42, "lomax": 63},
                    {"name": "Black_Sea", "lamin": 41, "lomin": 27, "lamax": 48, "lomax": 42},
                    {"name": "South_China_Sea", "lamin": 0, "lomin": 99, "lamax": 23, "lomax": 121}
                ]
                
                async with async_session_maker() as session:
                    # Clear old anomalies (keep last 24h only)
                    cutoff_time = datetime.utcnow() - timedelta(hours=24)
                    await session.execute(
                        delete(ThermalAnomaly).where(ThermalAnomaly.scan_time < cutoff_time)
                    )
                    
                    total_anomalies = 0
                    
                    for region in regions:
                        # VIIRS NOAA-20 NRT data for last 24 hours
                        url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{api_key}/VIIRS_NOAA20_NRT/{region['lomin']},{region['lamin']},{region['lomax']},{region['lamax']}/1"
                        
                        response = await self.client.get(url)
                        
                        if response.status_code == 200:
                            lines = response.text.strip().split('\n')
                            
                            if len(lines) > 1:  # Has data beyond header
                                for line in lines[1:]:  # Skip header
                                    parts = line.split(',')
                                    if len(parts) >= 10:
                                        try:
                                            lat = float(parts[0])
                                            lon = float(parts[1])
                                            brightness = float(parts[2])
                                            scan_time = datetime.strptime(parts[5] + parts[6], '%Y-%m-%d%H%M')
                                            satellite = parts[7]
                                            confidence = int(parts[8]) if parts[8].isdigit() else 0
                                            
                                            # Only store high-confidence anomalies
                                            if confidence >= 50:
                                                anomaly = ThermalAnomaly(
                                                    latitude=lat,
                                                    longitude=lon,
                                                    brightness=brightness,
                                                    scan_time=scan_time,
                                                    satellite=satellite,
                                                    confidence=confidence,
                                                    geom=from_shape(Point(lon, lat), srid=4326)
                                                )
                                                session.add(anomaly)
                                                total_anomalies += 1
                                        
                                        except (ValueError, IndexError) as e:
                                            continue
                    
                    await session.commit()
                    print(f"Updated {total_anomalies} thermal anomalies across {len(regions)} regions")
            
            except Exception as e:
                print(f"Thermal polling error: {e}")
            
            await asyncio.sleep(300)  # Poll every 5 minutes
