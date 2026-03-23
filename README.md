# OpenPalantir

A modular OSINT dashboard integrating NASA FIRMS, OpenSky, and Maritime AIS feeds into a unified 3D globe. Monitoring geopolitical flashpoints via automated geofencing and thermal anomaly detection.

## Architecture

- **Backend**: FastAPI + PostGIS for spatial queries
- **Frontend**: Next.js + Mapbox GL for 3D globe visualization
- **Database**: PostgreSQL with PostGIS extension
- **Data Sources**: OpenSky Network (Aviation), NASA FIRMS (Thermal), GDELT (Events)

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Mapbox API token (free tier: https://account.mapbox.com/)
- NASA FIRMS API key (optional - get it here: https://firms.modaps.eosdis.nasa.gov/api/area/)

### Demo Mode (No API Keys Required)

The portal includes realistic mock data for immediate testing:

```bash
# Set environment variable for mock mode
export USE_MOCK_DATA=true

# Start the stack
docker-compose up --build
```

Access the portal at http://localhost:3000 - you'll see:
- 10 sample aircraft including military callsigns (RCH, CNV, REACH, SPAR)
- 8 thermal anomalies in conflict zones (Iraq, Syria, Yemen, Crimea)
- Real-time alerts based on proximity detection
- Full UI functionality with sample data

### Live Mode (With API Keys)

1. Get your NASA FIRMS API key:
   - Visit https://firms.modaps.eosdis.nasa.gov/api/area/
   - Request a free API key (instant approval)

2. Add your Mapbox token to `frontend/components/WorldMap.tsx`:
```typescript
const MAPBOX_TOKEN = 'your_token_here'
```

3. Configure environment:
```bash
export NASA_FIRMS_API_KEY=your_key
export USE_MOCK_DATA=false
```

4. Start the stack:
```bash
docker-compose up --build
```

### Switching Between Modes

The system automatically detects API availability:
- If APIs are unavailable, it falls back to mock data
- Check the status indicator in the top-right corner
- Yellow badge = Demo Mode (mock data)
- Green badge = Live Mode (real APIs)

### Access Points
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- System Status: http://localhost:8000/api/system/status

## Features

### Current
- Real-time aviation tracking (Middle East region)
- NASA FIRMS thermal anomaly detection (3 conflict zones)
- Intelligent alert system with proximity detection
- Geofencing around 9 sensitive locations (airbases, nuclear sites, chokepoints)
- Mock data mode for development/demo (no API keys required)
- Automatic fallback to mock data when APIs unavailable
- System status indicator showing data source mode
- Tactical dark-mode UI with alert sidebar
- Timeline scrubber (72-hour window)
- GeoJSON-based data pipeline
- PostGIS spatial queries

### Mock Data Includes
- 10 realistic aircraft positions with military callsigns
- 8 thermal anomalies in active conflict zones
- Historical data simulation for timeline testing
- Automatic alert generation based on proximity rules

### Roadmap
- Maritime AIS integration (Spire/Datalastic)
- GDELT geopolitical event clustering
- Historical playback (functional timeline)
- WebSocket real-time updates
- Click handlers for detailed entity info
- Layer toggles (show/hide data sources)

## Data Layers

| Layer | Source | Update Frequency | Status |
|-------|--------|------------------|--------|
| Aviation | OpenSky Network | 30s | ✅ Active |
| Maritime | AIS (TBD) | 60s | 🔄 Planned |
| Thermal | NASA FIRMS | 5m | ✅ Active |
| Events | GDELT | 15m | 🔄 Planned |
| Alerts | Internal | Real-time | ✅ Active |

## Intelligence Logic

The system monitors for:
- Military aircraft callsigns (RCH, CNV, REACH, SPAR, etc.)
- Thermal anomalies within 5km of sensitive locations
- High-confidence (>70%) thermal events near nuclear facilities and airbases
- Aircraft within 50km of monitored locations
- Event clustering in flashpoint regions

### Monitored Locations
- Al Udeid Air Base (Qatar)
- Al Dhafra Air Base (UAE)
- Incirlik Air Base (Turkey)
- Strait of Hormuz (Iran/Oman)
- Bosphorus Strait (Turkey)
- Sevastopol Naval Base (Crimea)
- Bushehr Nuclear Plant (Iran)
- Natanz Nuclear Facility (Iran)
- Diego Garcia (UK/US)

## Development

### Backend
```bash
cd backend
pip install -r requirements.txt

# Run with mock data
export USE_MOCK_DATA=true
uvicorn main:app --reload

# Run with live APIs
export USE_MOCK_DATA=false
export NASA_FIRMS_API_KEY=your_key
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables

Backend (.env):
```
DATABASE_URL=postgresql://geoint:geoint_dev@localhost:5432/geoint
NASA_FIRMS_API_KEY=your_api_key_here
USE_MOCK_DATA=true  # Set to false for live data
```

## Security Notes

- This is an MVP using public OSINT sources
- No classified data should be ingested
- Rate limits apply to free-tier APIs
- Implement authentication before production deployment
