from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import engine, get_db
from app.models import Event
from app.schemas import EventCreate, EventRead


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connectivity only — schema comes from Alembic migrations
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
    yield
    await engine.dispose()


app = FastAPI(title="Obsero API", lifespan=lifespan)

# Browser on :3000 → API on :8000 is cross-origin; curl/SDK never need this.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
