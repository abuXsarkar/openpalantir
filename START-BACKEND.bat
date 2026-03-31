@echo off
echo ========================================
echo   OpenPalantir Backend (Demo Mode)
echo ========================================
echo.

cd backend

echo [1/3] Installing dependencies...
pip install -q fastapi uvicorn sqlalchemy httpx pydantic pydantic-settings python-dotenv geojson shapely aiosqlite

echo.
echo [2/3] Setting environment...
set USE_MOCK_DATA=true
set DATABASE_URL=sqlite+aiosqlite:///./geoint.db

echo.
echo [3/3] Starting server...
echo.
echo Backend running at: http://localhost:8000
echo API Docs at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop
echo.

python -m uvicorn main_lite:app --reload --host 0.0.0.0 --port 8000
