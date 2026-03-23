"""
Data source manager that seamlessly switches between mock and live data.
Automatically falls back to mock data when APIs are unavailable.
"""
import os
from typing import Optional, List, Dict
import httpx
from datetime import datetime
from services.mock_data import mock_generator

class DataSourceManager:
    """Manages data sources with automatic fallback to mock data"""
    
    def __init__(self):
        self.use_mock_data = os.getenv("USE_MOCK_DATA", "false").lower() == "true"
        self.nasa_api_key = os.getenv("NASA_FIRMS_API_KEY")
        self.client = httpx.AsyncClient(timeout=30.0)
        
        # Track API availability
        self.opensky_available = True
        self.nasa_available = bool(self.nasa_api_key and self.nasa_api_key != "your_api_key_here")
        
        print(f"Data Source Manager initialized:")
        print(f"  - Mock mode: {self.use_mock_data}")
        print(f"  - OpenSky API: {'Available' if self.opensky_available else 'Mock'}")
        print(f"  - NASA FIRMS: {'Available' if self.nasa_available else 'Mock'}")
    
    async def get_aircraft_data(self, lamin: float, lomin: float, lamax: float, lomax: float) -> List[Dict]:
        """Get aircraft data from OpenSky or mock source"""
        
        if self.use_mock_data or not self.opensky_available:
            print("Using mock aircraft data")
            return mock_generator.generate_aircraft_data()
        
        try:
            response = await self.client.get(
                "https://opensky-network.org/api/states/all",
                params={"lamin": lamin, "lomin": lomin, "lamax": lamax, "lomax": lomax}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("states"):
                    aircraft = []
                    for state in data["states"]:
                        if state[5] and state[6]:  # Has lat/lon
                            aircraft.append({
                                'icao24': state[0],
                                'callsign': state[1].strip() if state[1] else None,
                                'country': state[2],
                                'time_position': state[3],
                                'last_contact': state[4],
                                'lon': state[5],
                                'lat': state[6],
                                'alt': state[7],
                                'vel': state[9],
                                'hdg': state[10]
                            })
                    return aircraft
            
            # Fallback to mock on error
            print(f"OpenSky API error (status {response.status_code}), using mock data")
            self.opensky_available = False
            return mock_generator.generate_aircraft_data()
        
        except Exception as e:
            print(f"OpenSky API exception: {e}, using mock data")
            self.opensky_available = False
            return mock_generator.generate_aircraft_data()
    
    async def get_thermal_data(self, region: Dict) -> List[Dict]:
        """Get thermal anomaly data from NASA FIRMS or mock source"""
        
        if self.use_mock_data or not self.nasa_available:
            print(f"Using mock thermal data for {region['name']}")
            return mock_generator.generate_thermal_data()
        
        try:
            url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{self.nasa_api_key}/VIIRS_NOAA20_NRT/{region['lomin']},{region['lamin']},{region['lomax']},{region['lamax']}/1"
            
            response = await self.client.get(url)
            
            if response.status_code == 200:
                lines = response.text.strip().split('\n')
                
                if len(lines) > 1:
                    anomalies = []
                    for line in lines[1:]:  # Skip header
                        parts = line.split(',')
                        if len(parts) >= 10:
                            try:
                                anomalies.append({
                                    'lat': float(parts[0]),
                                    'lon': float(parts[1]),
                                    'brightness': float(parts[2]),
                                    'scan_time': datetime.strptime(parts[5] + parts[6], '%Y-%m-%d%H%M'),
                                    'satellite': parts[7],
                                    'confidence': int(parts[8]) if parts[8].isdigit() else 0
                                })
                            except (ValueError, IndexError):
                                continue
                    
                    if anomalies:
                        return anomalies
            
            # Fallback to mock
            print(f"NASA FIRMS API error (status {response.status_code}), using mock data")
            return mock_generator.generate_thermal_data()
        
        except Exception as e:
            print(f"NASA FIRMS API exception: {e}, using mock data")
            return mock_generator.generate_thermal_data()
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

# Singleton instance
data_source_manager = DataSourceManager()
