"""Simplified main.py for local development without PostGIS"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from routers import aviation_lite, thermal_lite, alerts_lite, system
from services.data_poller_lite import DataPoller
from database_lite import init_db

poller = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global poller
    await init_db()
    poller = DataPoller()
    asyncio.create_task(poller.start_polling())
    yield
    if poller:
        await poller.stop_polling()

app = FastAPI(title="GEOINT Portal API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(aviation_lite.router, prefix="/api/aviation", tags=["aviation"])
app.include_router(thermal_lite.router, prefix="/api/thermal", tags=["thermal"])
app.include_router(alerts_lite.router, prefix="/api/alerts", tags=["alerts"])
app.include_router(system.router, prefix="/api/system", tags=["system"])

@app.get("/")
async def root():
    return {"status": "GEOINT Portal API Online"}

@app.get("/api/health")
async def health():
    return {"status": "healthy"}
