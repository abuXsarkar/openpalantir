from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from routers import aviation, maritime, thermal, events, alerts, system
from services.data_poller import DataPoller
from database import init_db

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

app.include_router(aviation.router, prefix="/api/aviation", tags=["aviation"])
app.include_router(maritime.router, prefix="/api/maritime", tags=["maritime"])
app.include_router(thermal.router, prefix="/api/thermal", tags=["thermal"])
app.include_router(events.router, prefix="/api/events", tags=["events"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["alerts"])
app.include_router(system.router, prefix="/api/system", tags=["system"])

@app.get("/")
async def root():
    return {"status": "GEOINT Portal API Online"}

@app.get("/api/health")
async def health():
    return {"status": "healthy"}
