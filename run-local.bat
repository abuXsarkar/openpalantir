@echo off
echo Installing OpenPalantir locally...
echo.

cd backend

echo Installing Python dependencies...
pip install -r requirements-lite.txt
pip install aiosqlite

echo.
echo Setting environment variables...
set USE_MOCK_DATA=true
set DATABASE_URL=sqlite+aiosqlite:///./geoint.db

echo.
echo Starting backend server...
echo Backend will be available at http://localhost:8000
echo.
python -m uvicorn main_lite:app --reload
