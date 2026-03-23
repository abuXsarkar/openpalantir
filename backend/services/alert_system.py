from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.functions import ST_Distance, ST_DWithin
from database import ThermalAnomaly, AircraftPosition
from datetime import datetime, timedelta

# Sensitive locations (military bases, ports, facilities)
SENSITIVE_LOCATIONS = [
    {"name": "Al Udeid Air Base", "lat": 25.1173, "lon": 51.3150, "country": "Qatar", "type": "airbase"},
    {"name": "Al Dhafra Air Base", "lat": 24.2482, "lon": 54.5478, "country": "UAE", "type": "airbase"},
    {"name": "Incirlik Air Base", "lat": 37.0021, "lon": 35.4259, "country": "Turkey", "type": "airbase"},
    {"name": "Diego Garcia", "lat": -7.3167, "lon": 72.4167, "country": "UK/US", "type": "naval"},
    {"name": "Strait of Hormuz", "lat": 26.5667, "lon": 56.2500, "country": "Iran/Oman", "type": "chokepoint"},
    {"name": "Bosphorus Strait", "lat": 41.1200, "lon": 29.0783, "country": "Turkey", "type": "chokepoint"},
    {"name": "Sevastopol Naval Base", "lat": 44.6167, "lon": 33.5333, "country": "Crimea", "type": "naval"},
    {"name": "Bushehr Nuclear Plant", "lat": 28.9933, "lon": 50.8783, "country": "Iran", "type": "nuclear"},
    {"name": "Natanz Nuclear Facility", "lat": 33.7242, "lon": 51.7281, "country": "Iran", "type": "nuclear"},
]

class AlertSystem:
    def __init__(self):
        self.alert_radius_km = 5.0  # 5km proximity threshold
        self.alert_cache = []
    
    async def check_thermal_proximity(self, session: AsyncSession):
        """Check if thermal anomalies are near sensitive locations"""
        alerts = []
        
        # Get recent high-confidence thermal anomalies (last 6 hours)
        cutoff_time = datetime.utcnow() - timedelta(hours=6)
        result = await session.execute(
            select(ThermalAnomaly).where(
                ThermalAnomaly.scan_time >= cutoff_time,
                ThermalAnomaly.confidence >= 70
            )
        )
        anomalies = result.scalars().all()
        
        for anomaly in anomalies:
            for location in SENSITIVE_LOCATIONS:
                # Calculate distance using Haversine formula
                distance = self._haversine_distance(
                    anomaly.latitude, anomaly.longitude,
                    location['lat'], location['lon']
                )
                
                if distance <= self.alert_radius_km:
                    alerts.append({
                        "type": "thermal_proximity",
                        "severity": "high" if location['type'] in ['nuclear', 'airbase'] else "medium",
                        "message": f"Thermal anomaly detected {distance:.2f}km from {location['name']}",
                        "location": location['name'],
                        "country": location['country'],
                        "coordinates": [anomaly.longitude, anomaly.latitude],
                        "brightness": anomaly.brightness,
                        "confidence": anomaly.confidence,
                        "timestamp": anomaly.scan_time.isoformat()
                    })
        
        return alerts
    
    async def check_aircraft_proximity(self, session: AsyncSession):
        """Check if military aircraft are near sensitive locations"""
        alerts = []
        
        # Get current aircraft positions
        result = await session.execute(select(AircraftPosition))
        aircraft = result.scalars().all()
        
        # Military callsign prefixes
        military_prefixes = ['RCH', 'CNV', 'EVAC', 'REACH', 'SPAR', 'JAKE', 'BOXER', 'NAVY']
        
        for plane in aircraft:
            if plane.callsign:
                callsign = plane.callsign.strip().upper()
                
                # Check if military aircraft
                is_military = any(callsign.startswith(prefix) for prefix in military_prefixes)
                
                if is_military:
                    for location in SENSITIVE_LOCATIONS:
                        distance = self._haversine_distance(
                            plane.latitude, plane.longitude,
                            location['lat'], location['lon']
                        )
                        
                        if distance <= 50:  # 50km radius for aircraft
                            alerts.append({
                                "type": "military_aircraft",
                                "severity": "medium",
                                "message": f"Military aircraft {callsign} detected {distance:.2f}km from {location['name']}",
                                "location": location['name'],
                                "country": location['country'],
                                "callsign": callsign,
                                "icao24": plane.icao24,
                                "altitude": plane.altitude,
                                "coordinates": [plane.longitude, plane.latitude],
                                "timestamp": datetime.utcnow().isoformat()
                            })
        
        return alerts
    
    async def get_all_alerts(self, session: AsyncSession):
        """Get all current alerts"""
        thermal_alerts = await self.check_thermal_proximity(session)
        aircraft_alerts = await self.check_aircraft_proximity(session)
        
        all_alerts = thermal_alerts + aircraft_alerts
        
        # Sort by severity
        severity_order = {"high": 0, "medium": 1, "low": 2}
        all_alerts.sort(key=lambda x: severity_order.get(x['severity'], 3))
        
        self.alert_cache = all_alerts
        return all_alerts
    
    def _haversine_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points in kilometers"""
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371  # Earth radius in kilometers
        
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c
