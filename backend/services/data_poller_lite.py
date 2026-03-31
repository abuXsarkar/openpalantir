import asyncio
from datetime import datetime, timedelta
from sqlalchemy import select, delete
from database_lite import async_session_maker, AircraftPosition, ThermalAnomaly
from services.data_source_manager import data_source_manager

class DataPoller:
    def __init__(self):
        self.running = False
    
    async def start_polling(self):
        self.running = True
        await asyncio.gather(
            self.poll_aviation(),
            self.poll_thermal()
        )
    
    async def stop_polling(self):
        self.running = False
        await data_source_manager.close()
    
    async def poll_aviation(self):
        """Poll OpenSky Network for aircraft positions"""
        while self.running:
            try:
                aircraft_data = await data_source_manager.get_aircraft_data(
                    lamin=12, lomin=25, lamax=42, lomax=63
                )
                
                async with async_session_maker() as session:
                    await session.execute(delete(AircraftPosition))
                    
                    for data in aircraft_data:
                        aircraft = AircraftPosition(
                            icao24=data['icao24'],
                            callsign=data.get('callsign'),
                            origin_country=data.get('country', 'Unknown'),
                            time_position=data.get('time_position', int(datetime.utcnow().timestamp())),
                            last_contact=data.get('last_contact', int(datetime.utcnow().timestamp())),
                            longitude=data['lon'],
                            latitude=data['lat'],
                            altitude=data.get('alt'),
                            velocity=data.get('vel'),
                            heading=data.get('hdg')
                        )
                        session.add(aircraft)
                    
                    await session.commit()
                    print(f"Updated {len(aircraft_data)} aircraft positions")
            
            except Exception as e:
                print(f"Aviation polling error: {e}")
            
            await asyncio.sleep(30)
    
    async def poll_thermal(self):
        """Poll NASA FIRMS for thermal anomalies"""
        regions = [
            {"name": "Middle_East", "lamin": 12, "lomin": 25, "lamax": 42, "lomax": 63},
            {"name": "Black_Sea", "lamin": 41, "lomin": 27, "lamax": 48, "lomax": 42},
            {"name": "South_China_Sea", "lamin": 0, "lomin": 99, "lamax": 23, "lomax": 121}
        ]
        
        while self.running:
            try:
                async with async_session_maker() as session:
                    cutoff_time = datetime.utcnow() - timedelta(hours=24)
                    await session.execute(
                        delete(ThermalAnomaly).where(ThermalAnomaly.scan_time < cutoff_time)
                    )
                    
                    total_anomalies = 0
                    
                    for region in regions:
                        thermal_data = await data_source_manager.get_thermal_data(region)
                        
                        for data in thermal_data:
                            if data.get('confidence', 0) >= 50:
                                anomaly = ThermalAnomaly(
                                    latitude=data['lat'],
                                    longitude=data['lon'],
                                    brightness=data['brightness'],
                                    scan_time=data['scan_time'],
                                    satellite=data.get('satellite', 'NOAA-20'),
                                    confidence=data['confidence']
                                )
                                session.add(anomaly)
                                total_anomalies += 1
                    
                    await session.commit()
                    print(f"Updated {total_anomalies} thermal anomalies")
            
            except Exception as e:
                print(f"Thermal polling error: {e}")
            
            await asyncio.sleep(300)
