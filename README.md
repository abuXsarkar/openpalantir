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
- NASA FIRMS API key (get it here: https://firms.modaps.eosdis.nasa.gov/api/area/)

### Setup

1. Get your NASA FIRMS API key:
   - Visit https://firms.modaps.eosdis.nasa.gov/api/area/
   - Request a free API key (instant approval)
   - Set it as environment variable: `export NASA_FIRMS_API_KEY=your_key`

2. Add your Mapbox token to `frontend/components/WorldMap.tsx`:
```typescript
const MAPBOX_TOKEN = 'your_token_here'
```

3. Start the stack:
```bash
docker-compose up --build
```

4. Access the portal:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Features

### Current
- Real-time aviation tracking (Middle East region)
- NASA FIRMS thermal anomaly detection (3 conflict zones)
- Intelligent alert system with proximity detection
- Geofencing around 9 sensitive locations (airbases, nuclear sites, chokepoints)
- Tactical dark-mode UI with alert sidebar
- Timeline scrubber (72-hour window)
- GeoJSON-based data pipeline
- PostGIS spatial queries

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
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Security Notes

- This is an MVP using public OSINT sources
- No classified data should be ingested
- Rate limits apply to free-tier APIs
- Implement authentication before production deployment
