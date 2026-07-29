"""Obsero FastAPI app — health + events ingest/list.

Schema is owned by Alembic (see migrations/). This module only checks
DB connectivity on startup and exposes HTTP endpoints.
"""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import engine, get_db
from app.models import Event
from app.schemas import EventBatchCreate, EventCreate, EventRead


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
    # Pass through all fields (LLM ones may be None for generic track() calls)
    event = Event(
        name=body.name,
        payload=body.payload,
        provider=body.provider,
        model=body.model,
        input=body.input,
        output=body.output,
        prompt_tokens=body.prompt_tokens,
        completion_tokens=body.completion_tokens,
        total_tokens=body.total_tokens,
        latency_ms=body.latency_ms,
        cost_usd=body.cost_usd,
        status=body.status,
    )
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


@app.post("/events/batch", response_model=list[EventRead], status_code=201)
async def create_events_batch(
    body: EventBatchCreate,
    db: AsyncSession = Depends(get_db),
):
    """Insert many events in one request (SDK flush path)."""
    rows: list[Event] = []
    for item in body.events:
        event = Event(
            name=item.name,
            payload=item.payload,
            provider=item.provider,
            model=item.model,
            input=item.input,
            output=item.output,
            prompt_tokens=item.prompt_tokens,
            completion_tokens=item.completion_tokens,
            total_tokens=item.total_tokens,
            latency_ms=item.latency_ms,
            cost_usd=item.cost_usd,
            status=item.status,
        )
        db.add(event)
        rows.append(event)
    await db.commit()
    for event in rows:
        await db.refresh(event)  # ids + created_at
    return rows
