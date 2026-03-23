from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://geoint:geoint_dev@localhost:5432/geoint").replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class AircraftPosition(Base):
    __tablename__ = "aircraft_positions"
    id = Column(Integer, primary_key=True)
    icao24 = Column(String, index=True)
    callsign = Column(String)
    origin_country = Column(String)
    time_position = Column(Integer)
    last_contact = Column(Integer)
    longitude = Column(Float)
    latitude = Column(Float)
    altitude = Column(Float)
    velocity = Column(Float)
    heading = Column(Float)
    geom = Column(Geometry('POINT', srid=4326))

class ThermalAnomaly(Base):
    __tablename__ = "thermal_anomalies"
    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    brightness = Column(Float)
    scan_time = Column(DateTime)
    satellite = Column(String)
    confidence = Column(Integer)
    geom = Column(Geometry('POINT', srid=4326))

class GeopoliticalEvent(Base):
    __tablename__ = "geopolitical_events"
    id = Column(Integer, primary_key=True)
    event_id = Column(String, unique=True)
    event_date = Column(DateTime)
    actor1 = Column(String)
    actor2 = Column(String)
    event_type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    goldstein_scale = Column(Float)
    source_url = Column(String)
    geom = Column(Geometry('POINT', srid=4326))

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
