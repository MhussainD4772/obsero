from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import engine, get_db
from app.models import Base, Event
from app.schemas import EventCreate, EventRead


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: touch DB (fails loudly if down) + create tables
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))  # connectivity check
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: dispose connection pool
    await engine.dispose()


app = FastAPI(title="Obsero API", lifespan=lifespan)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/events", response_model=EventRead, status_code=201)
async def create_event(
    body: EventCreate,
    db: AsyncSession = Depends(get_db),
):
    event = Event(name=body.name, payload=body.payload)
    db.add(event)
    await db.commit()
    await db.refresh(event)  # pull id + created_at from Postgres
    return event


@app.get("/events", response_model=list[EventRead])
async def list_events(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Event).order_by(Event.created_at.desc()))
    return result.scalars().all()
