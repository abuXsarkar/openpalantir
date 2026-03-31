"""Ultra-simple backend that just serves mock data without database"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.mock_data import mock_generator
from services.alert_system_lite import AlertSystem, SENSITIVE_LOCATIONS
from datetime import datetime

app = FastAPI(title="GEOINT Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

alert_system = AlertSystem()

@app.get("/")
async def root():
    return {"status": "GEOINT Portal API Online", "mode": "mock"}

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/aviation/positions")
async def get_aircraft():
    """Get aircraft positions"""
    aircraft = mock_generator.generate_aircraft_data()
    
    features = []
    for data in aircraft:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [data['lon'], data['lat']]
            },
            "properties": {
                "icao24": data['icao24'],
                "callsign": data.get('callsign'),
                "country": data.get('country', 'Unknown'),
                "altitude": data.get('alt'),
                "velocity": data.get('vel'),
                "heading": data.get('hdg'),
                "type": "aircraft"
            }
        })
    
    return {
        "type": "FeatureCollection",
        "features": features
    }

@app.get("/api/thermal/anomalies")
async def get_thermal():
    """Get thermal anomalies"""
    anomalies = mock_generator.generate_thermal_data()
    
    features = []
    for anomaly in anomalies:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [anomaly['lon'], anomaly['lat']]
            },
            "properties": {
                "brightness": anomaly['brightness'],
                "confidence": anomaly['confidence'],
                "satellite": anomaly.get('satellite', 'NOAA-20'),
                "scan_time": anomaly['scan_time'].isoformat(),
                "type": "thermal"
            }
        })
    
    return {
        "type": "FeatureCollection",
        "features": features
    }

@app.get("/api/alerts/locations")
async def get_locations():
    """Get sensitive locations"""
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

@app.get("/api/alerts/current")
async def get_alerts():
    """Get current alerts"""
    # Generate simple alerts from mock data
    aircraft = mock_generator.generate_aircraft_data()
    thermal = mock_generator.generate_thermal_data()
    
    alerts = []
    
    # Check for military aircraft
    military_prefixes = ['RCH', 'CNV', 'REACH', 'SPAR', 'NAVY']
    for plane in aircraft:
        callsign = plane.get('callsign', '').strip().upper()
        if any(callsign.startswith(prefix) for prefix in military_prefixes):
            alerts.append({
                "type": "military_aircraft",
                "severity": "medium",
                "message": f"Military aircraft {callsign} detected near {plane.get('country', 'Unknown')}",
                "location": plane.get('country', 'Unknown'),
                "callsign": callsign,
                "coordinates": [plane['lon'], plane['lat']],
                "timestamp": datetime.utcnow().isoformat()
            })
    
    # Check for high-confidence thermal anomalies
    for anomaly in thermal:
        if anomaly.get('confidence', 0) >= 80:
            alerts.append({
                "type": "thermal_proximity",
                "severity": "high",
                "message": f"High-confidence thermal anomaly detected in {anomaly.get('region', 'conflict zone')}",
                "location": anomaly.get('region', 'Unknown'),
                "brightness": anomaly['brightness'],
                "confidence": anomaly['confidence'],
                "coordinates": [anomaly['lon'], anomaly['lat']],
                "timestamp": anomaly['scan_time'].isoformat()
            })
    
    return {
        "count": len(alerts),
        "alerts": alerts
    }

@app.get("/api/maritime/vessels")
async def get_vessels():
    """Get maritime vessel positions (AIS data)"""
    vessels = mock_generator.generate_maritime_data()
    
    features = []
    for vessel in vessels:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [vessel['lon'], vessel['lat']]
            },
            "properties": {
                "mmsi": vessel['mmsi'],
                "name": vessel['name'],
                "type": vessel['type'],
                "speed": vessel['speed'],
                "course": vessel['course'],
                "flag": vessel['flag'],
                "destination": vessel['destination'],
                "vessel_type": "vessel"
            }
        })
    
    return {
        "type": "FeatureCollection",
        "features": features
    }

@app.get("/api/satellites/tracking")
async def get_satellites():
    """Get satellite tracking data"""
    satellites = mock_generator.generate_satellite_data()
    
    features = []
    for sat in satellites:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [sat['lon'], sat['lat']]
            },
            "properties": {
                "norad_id": sat['norad_id'],
                "name": sat['name'],
                "altitude": sat['alt'],
                "velocity": sat['velocity'],
                "type": sat['type'],
                "satellite_type": "satellite"
            }
        })
    
    return {
        "type": "FeatureCollection",
        "features": features
    }

@app.get("/api/cyber/incidents")
async def get_cyber_incidents():
    """Get cyber security incidents"""
    incidents = mock_generator.generate_cyber_events()
    
    features = []
    for incident in incidents:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [incident['lon'], incident['lat']]
            },
            "properties": {
                "city": incident['city'],
                "country": incident['country'],
                "type": incident['type'],
                "severity": incident['severity'],
                "target": incident['target'],
                "timestamp": incident['timestamp'].isoformat(),
                "incident_type": "cyber"
            }
        })
    
    return {
        "type": "FeatureCollection",
        "features": features
    }

@app.get("/api/military/bases")
async def get_military_bases():
    """Get military installations"""
    bases = mock_generator.generate_military_bases()
    
    features = []
    for base in bases:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [base['lon'], base['lat']]
            },
            "properties": {
                "name": base['name'],
                "country": base['country'],
                "type": base['type'],
                "status": base['status'],
                "base_type": "military"
            }
        })
    
    return {
        "type": "FeatureCollection",
        "features": features
    }

@app.get("/api/system/status")
async def get_status():
    """Get system status"""
    return {
        "status": "operational",
        "data_sources": {
            "mode": "mock",
            "opensky": {
                "available": False,
                "status": "using_mock"
            },
            "nasa_firms": {
                "available": False,
                "status": "using_mock"
            },
            "maritime_ais": {
                "available": False,
                "status": "using_mock"
            },
            "satellite_tracking": {
                "available": False,
                "status": "using_mock"
            }
        },
        "layers": {
            "aviation": True,
            "thermal": True,
            "maritime": True,
            "satellites": True,
            "cyber": True,
            "military_bases": True
        }
    }
