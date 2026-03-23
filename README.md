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
- NASA FIRMS API key (optional, for thermal data: https://firms.modaps.eosdis.nasa.gov/api/)

### Setup

1. Add your Mapbox token to `frontend/components/WorldMap.tsx`:
```typescript
const MAPBOX_TOKEN = 'your_token_here'
```

2. (Optional) Add NASA FIRMS API key to `backend/services/data_poller.py`

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
- Tactical dark-mode UI with alert sidebar
- Timeline scrubber (72-hour window)
- GeoJSON-based data pipeline
- PostGIS spatial queries

### Roadmap
- Maritime AIS integration (Spire/Datalastic)
- NASA FIRMS thermal anomaly detection
- GDELT geopolitical event clustering
- Conflict alert system (proximity-based)
- Heatmap visualization for tension zones

## Data Layers

| Layer | Source | Update Frequency | Status |
|-------|--------|------------------|--------|
| Aviation | OpenSky Network | 30s | ✅ Active |
| Maritime | AIS (TBD) | 60s | 🔄 Planned |
| Thermal | NASA FIRMS | 5m | 🔄 Planned |
| Events | GDELT | 15m | 🔄 Planned |

## Intelligence Logic

The system monitors for:
- Military aircraft callsigns (RCH, CNV prefixes)
- Thermal anomalies near sensitive locations
- Event clustering in flashpoint regions

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
