"""
Mock data generator for development and demo purposes.
Provides realistic sample data when APIs are unavailable.
"""
from datetime import datetime, timedelta
import random
from typing import List, Dict

class MockDataGenerator:
    """Generate realistic mock data for GEOINT portal"""
    
    # Real historical data points from public sources
    SAMPLE_AIRCRAFT = [
        {"icao24": "ae01ce", "callsign": "RCH863", "country": "United States", "lat": 26.2656, "lon": 50.6330, "alt": 35000, "vel": 450, "hdg": 285},
        {"icao24": "ae04c5", "callsign": "RCH134", "country": "United States", "lat": 29.3117, "lon": 47.4818, "alt": 38000, "vel": 480, "hdg": 90},
        {"icao24": "ae0443", "callsign": "CNV4523", "country": "United States", "lat": 25.8103, "lon": 55.9659, "alt": 5000, "vel": 250, "hdg": 180},
        {"icao24": "ae5c4e", "callsign": "REACH71", "country": "United States", "lat": 37.2389, "lon": 35.5211, "alt": 32000, "vel": 470, "hdg": 315},
        {"icao24": "43c6e2", "callsign": "UAE231", "country": "United Arab Emirates", "lat": 24.4539, "lon": 54.3773, "alt": 28000, "vel": 420, "hdg": 45},
        {"icao24": "738001", "callsign": "QTR8342", "country": "Qatar", "lat": 25.2731, "lon": 51.6080, "alt": 15000, "vel": 320, "hdg": 270},
        {"icao24": "4ca854", "callsign": "THY7", "country": "Turkey", "lat": 40.9769, "lon": 28.8146, "alt": 37000, "vel": 490, "hdg": 135},
        {"icao24": "710258", "callsign": "SWR154", "country": "Saudi Arabia", "lat": 21.6792, "lon": 39.1564, "alt": 33000, "vel": 460, "hdg": 225},
        {"icao24": "ae09b4", "callsign": "SPAR19", "country": "United States", "lat": 33.3128, "lon": 44.3615, "alt": 29000, "vel": 440, "hdg": 180},
        {"icao24": "ae1234", "callsign": "NAVY12", "country": "United States", "lat": 26.5667, "lon": 56.2500, "alt": 8000, "vel": 280, "hdg": 90},
    ]
    
    # Real thermal anomaly locations from conflict zones (based on historical FIRMS data)
    SAMPLE_THERMAL = [
        {"lat": 33.3152, "lon": 44.3661, "brightness": 345.2, "confidence": 85, "satellite": "NOAA-20", "region": "Iraq"},
        {"lat": 36.2021, "lon": 37.1343, "brightness": 328.7, "confidence": 78, "satellite": "NOAA-20", "region": "Syria"},
        {"lat": 32.5149, "lon": 44.4205, "brightness": 312.4, "confidence": 72, "satellite": "NOAA-20", "region": "Iraq"},
        {"lat": 35.9213, "lon": 36.0108, "brightness": 298.9, "confidence": 81, "satellite": "NOAA-20", "region": "Syria"},
        {"lat": 44.5833, "lon": 33.5167, "brightness": 356.1, "confidence": 89, "satellite": "NOAA-20", "region": "Crimea"},
        {"lat": 46.9750, "lon": 31.9944, "brightness": 341.3, "confidence": 76, "satellite": "NOAA-20", "region": "Ukraine"},
        {"lat": 28.9933, "lon": 50.8783, "brightness": 302.5, "confidence": 74, "satellite": "NOAA-20", "region": "Iran"},
        {"lat": 12.8628, "lon": 45.0369, "brightness": 318.6, "confidence": 83, "satellite": "NOAA-20", "region": "Yemen"},
    ]
    
    # Maritime vessels (AIS data simulation)
    SAMPLE_VESSELS = [
        {"mmsi": "636019825", "name": "IRAN SHAHED", "type": "Tanker", "lat": 26.5667, "lon": 56.2500, "speed": 12.3, "course": 285, "flag": "Iran", "destination": "Bandar Abbas"},
        {"mmsi": "477995900", "name": "HONG KONG TRADER", "type": "Cargo", "lat": 22.3193, "lon": 114.1694, "speed": 8.5, "course": 180, "flag": "Hong Kong", "destination": "Singapore"},
        {"mmsi": "636092456", "name": "GRACE 1", "type": "Tanker", "lat": 36.1408, "lon": -5.3536, "speed": 0.0, "course": 0, "flag": "Iran", "destination": "Gibraltar"},
        {"mmsi": "273353800", "name": "ADMIRAL GRIGOROVICH", "type": "Military", "lat": 44.6167, "lon": 33.5333, "speed": 15.2, "course": 90, "flag": "Russia", "destination": "Sevastopol"},
        {"mmsi": "538006090", "name": "USS ABRAHAM LINCOLN", "type": "Military", "lat": 25.2867, "lon": 55.3644, "speed": 18.0, "course": 270, "flag": "USA", "destination": "Persian Gulf"},
        {"mmsi": "477123456", "name": "COSCO SHIPPING", "type": "Container", "lat": 1.2897, "lon": 103.8501, "speed": 14.5, "course": 45, "flag": "China", "destination": "Shanghai"},
        {"mmsi": "636019999", "name": "SABITI", "type": "Tanker", "lat": 27.1833, "lon": 56.2667, "speed": 10.1, "course": 315, "flag": "Iran", "destination": "Jeddah"},
        {"mmsi": "229767000", "name": "FS CHARLES DE GAULLE", "type": "Military", "lat": 35.5000, "lon": 33.0000, "speed": 12.0, "course": 180, "flag": "France", "destination": "Eastern Med"},
    ]
    
    # Satellite passes (ISS, reconnaissance, imaging satellites)
    SAMPLE_SATELLITES = [
        {"norad_id": "25544", "name": "ISS (ZARYA)", "lat": 28.5, "lon": 51.2, "alt": 408, "velocity": 7.66, "type": "Space Station"},
        {"norad_id": "43013", "name": "USA 290 (KH-11)", "lat": 33.3, "lon": 44.4, "alt": 270, "velocity": 7.8, "type": "Reconnaissance"},
        {"norad_id": "37348", "name": "COSMO-SKYMED 1", "lat": 36.2, "lon": 37.1, "alt": 619, "velocity": 7.5, "type": "SAR Imaging"},
        {"norad_id": "40732", "name": "GAOFEN-2", "lat": 26.5, "lon": 56.3, "alt": 631, "velocity": 7.5, "type": "Optical Imaging"},
        {"norad_id": "44506", "name": "USA 314 (TOPAZ)", "lat": 44.6, "lon": 33.5, "alt": 1000, "velocity": 7.3, "type": "SIGINT"},
        {"norad_id": "41866", "name": "SENTINEL-1B", "lat": 35.0, "lon": 35.0, "alt": 693, "velocity": 7.5, "type": "SAR Imaging"},
    ]
    
    # Cyber incidents and infrastructure monitoring
    SAMPLE_CYBER_EVENTS = [
        {"lat": 35.6892, "lon": 51.3890, "city": "Tehran", "country": "Iran", "type": "DDoS Attack", "severity": "high", "target": "Government Infrastructure"},
        {"lat": 55.7558, "lon": 37.6173, "city": "Moscow", "country": "Russia", "type": "Data Breach", "severity": "medium", "target": "Energy Sector"},
        {"lat": 31.2304, "lon": 121.4737, "city": "Shanghai", "country": "China", "type": "APT Activity", "severity": "high", "target": "Defense Contractors"},
        {"lat": 33.8869, "lon": 35.5131, "city": "Beirut", "country": "Lebanon", "type": "Malware Campaign", "severity": "medium", "target": "Banking Sector"},
    ]
    
    # Military installations and bases
    SAMPLE_MILITARY_BASES = [
        {"name": "Natanz Nuclear Facility", "lat": 33.7242, "lon": 51.7281, "country": "Iran", "type": "Nuclear", "status": "Active"},
        {"name": "Fordow Fuel Enrichment Plant", "lat": 34.9564, "lon": 50.9864, "country": "Iran", "type": "Nuclear", "status": "Active"},
        {"name": "Khmeimim Air Base", "lat": 35.4017, "lon": 35.9489, "country": "Syria", "type": "Airbase", "status": "Active"},
        {"name": "Tartus Naval Base", "lat": 34.8833, "lon": 35.8833, "country": "Syria", "type": "Naval", "status": "Active"},
        {"name": "Hmeimim Air Base", "lat": 35.4017, "lon": 35.9489, "country": "Syria", "type": "Airbase", "status": "Active"},
    ]
    
    def __init__(self):
        self.time_offset = 0  # For simulating time progression
    
    def generate_aircraft_data(self, count: int = 10) -> List[Dict]:
        """Generate realistic aircraft position data"""
        aircraft = []
        base_time = int(datetime.utcnow().timestamp())
        
        for i in range(min(count, len(self.SAMPLE_AIRCRAFT))):
            sample = self.SAMPLE_AIRCRAFT[i].copy()
            
            # Add slight random variations to make it look live
            sample['lat'] += random.uniform(-0.5, 0.5)
            sample['lon'] += random.uniform(-0.5, 0.5)
            sample['alt'] += random.uniform(-1000, 1000)
            sample['vel'] += random.uniform(-20, 20)
            sample['hdg'] = (sample['hdg'] + random.uniform(-10, 10)) % 360
            sample['time_position'] = base_time - random.randint(0, 30)
            sample['last_contact'] = base_time
            
            aircraft.append(sample)
        
        return aircraft
    
    def generate_thermal_data(self, hours_back: int = 6) -> List[Dict]:
        """Generate realistic thermal anomaly data"""
        anomalies = []
        base_time = datetime.utcnow()
        
        for sample in self.SAMPLE_THERMAL:
            # Create anomalies at different times in the past
            time_offset = random.randint(0, hours_back * 60)
            scan_time = base_time - timedelta(minutes=time_offset)
            
            anomaly = sample.copy()
            anomaly['scan_time'] = scan_time
            
            # Add slight variations
            anomaly['lat'] += random.uniform(-0.05, 0.05)
            anomaly['lon'] += random.uniform(-0.05, 0.05)
            anomaly['brightness'] += random.uniform(-10, 10)
            
            anomalies.append(anomaly)
        
        return anomalies
    
    def generate_maritime_data(self, count: int = 8) -> List[Dict]:
        """Generate realistic maritime vessel data"""
        vessels = []
        
        for i in range(min(count, len(self.SAMPLE_VESSELS))):
            sample = self.SAMPLE_VESSELS[i].copy()
            
            # Add slight variations
            sample['lat'] += random.uniform(-0.1, 0.1)
            sample['lon'] += random.uniform(-0.1, 0.1)
            sample['speed'] += random.uniform(-1, 1)
            sample['course'] = (sample['course'] + random.uniform(-5, 5)) % 360
            sample['timestamp'] = datetime.utcnow()
            
            vessels.append(sample)
        
        return vessels
    
    def generate_satellite_data(self, count: int = 6) -> List[Dict]:
        """Generate satellite tracking data"""
        satellites = []
        
        for i in range(min(count, len(self.SAMPLE_SATELLITES))):
            sample = self.SAMPLE_SATELLITES[i].copy()
            
            # Simulate orbital movement
            sample['lat'] += random.uniform(-2, 2)
            sample['lon'] += random.uniform(-5, 5)
            sample['timestamp'] = datetime.utcnow()
            
            satellites.append(sample)
        
        return satellites
    
    def generate_cyber_events(self, count: int = 4) -> List[Dict]:
        """Generate cyber incident data"""
        events = []
        base_time = datetime.utcnow()
        
        for i in range(min(count, len(self.SAMPLE_CYBER_EVENTS))):
            event = self.SAMPLE_CYBER_EVENTS[i].copy()
            event['timestamp'] = base_time - timedelta(hours=random.randint(1, 24))
            events.append(event)
        
        return events
    
    def generate_military_bases(self) -> List[Dict]:
        """Generate military installation data"""
        return self.SAMPLE_MILITARY_BASES.copy()
    
    def generate_geopolitical_events(self, count: int = 5) -> List[Dict]:
        """Generate sample geopolitical events"""
        events = [
            {"event_id": "GE001", "lat": 33.3128, "lon": 44.3615, "actor1": "Iraq", "actor2": "ISIS", 
             "event_type": "Armed Conflict", "goldstein_scale": -8.0, "source_url": "https://example.com"},
            {"event_id": "GE002", "lat": 36.2021, "lon": 37.1343, "actor1": "Syria", "actor2": "Rebels", 
             "event_type": "Military Action", "goldstein_scale": -7.5, "source_url": "https://example.com"},
            {"event_id": "GE003", "lat": 26.5667, "lon": 56.2500, "actor1": "Iran", "actor2": "US", 
             "event_type": "Diplomatic Tension", "goldstein_scale": -5.0, "source_url": "https://example.com"},
            {"event_id": "GE004", "lat": 44.5833, "lon": 33.5167, "actor1": "Russia", "actor2": "Ukraine", 
             "event_type": "Military Mobilization", "goldstein_scale": -9.0, "source_url": "https://example.com"},
            {"event_id": "GE005", "lat": 12.8628, "lon": 45.0369, "actor1": "Yemen", "actor2": "Saudi Arabia", 
             "event_type": "Border Incident", "goldstein_scale": -6.5, "source_url": "https://example.com"},
        ]
        
        base_time = datetime.utcnow()
        for i, event in enumerate(events[:count]):
            event['event_date'] = base_time - timedelta(hours=random.randint(1, 48))
        
        return events[:count]
    
    def get_historical_aircraft_track(self, icao24: str, hours: int = 24) -> List[Dict]:
        """Generate historical track for an aircraft"""
        track = []
        base_time = datetime.utcnow()
        
        # Find the aircraft in samples
        aircraft = next((a for a in self.SAMPLE_AIRCRAFT if a['icao24'] == icao24), None)
        if not aircraft:
            return []
        
        # Generate positions every 5 minutes for the past N hours
        for i in range(0, hours * 12):
            timestamp = base_time - timedelta(minutes=i * 5)
            
            # Simulate movement along heading
            lat_offset = (i * 0.01) * (1 if aircraft['hdg'] < 180 else -1)
            lon_offset = (i * 0.01) * (1 if 90 < aircraft['hdg'] < 270 else -1)
            
            track.append({
                'timestamp': timestamp,
                'lat': aircraft['lat'] + lat_offset,
                'lon': aircraft['lon'] + lon_offset,
                'alt': aircraft['alt'] + random.uniform(-500, 500),
                'vel': aircraft['vel'] + random.uniform(-10, 10)
            })
        
        return track

# Singleton instance
mock_generator = MockDataGenerator()
