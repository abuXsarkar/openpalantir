# Quick Start Guide - OpenPalantir

## Option 1: Backend Only (Works Now!)

You can run just the backend API to see the data:

1. Double-click `START-BACKEND.bat`
2. Wait for "Application startup complete"
3. Open browser to http://localhost:8000/docs
4. Try the API endpoints:
   - `/api/aviation/positions` - See aircraft data
   - `/api/thermal/anomalies` - See thermal data
   - `/api/alerts/current` - See active alerts
   - `/api/system/status` - Check system status

## Option 2: Full Stack (Requires Node.js)

### Install Node.js First
1. Download from https://nodejs.org/ (LTS version)
2. Install and restart terminal
3. Verify: `node --version`

### Start Backend
```bash
# In terminal 1
cd backend
pip install -r requirements-lite.txt
pip install aiosqlite
set USE_MOCK_DATA=true
set DATABASE_URL=sqlite+aiosqlite:///./geoint.db
python -m uvicorn main_lite:app --reload
```

### Start Frontend
```bash
# In terminal 2
cd frontend
npm install
npm run dev
```

### Access
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Option 3: Docker (Easiest - Requires Docker Desktop)

1. Install Docker Desktop from https://www.docker.com/products/docker-desktop/
2. Run: `docker-compose up --build`
3. Access: http://localhost:3000

## Demo Mode

The system runs in DEMO MODE by default with realistic mock data:
- 10 aircraft positions (including military)
- 8 thermal anomalies in conflict zones
- Real-time alerts
- No API keys required!

Look for the yellow "DEMO MODE" badge in the top-right corner.

## Troubleshooting

### "uvicorn not found"
Run: `pip install uvicorn`

### "npm not found"
Install Node.js from https://nodejs.org/

### "psycopg2 error"
Use `requirements-lite.txt` instead of `requirements.txt`

### Port already in use
Change ports in the commands:
- Backend: `--port 8001`
- Frontend: Edit `package.json` to use different port
