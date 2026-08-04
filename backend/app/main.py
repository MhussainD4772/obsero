"""Obsero FastAPI app — health, events, nested trace ingest + query.

Schema is owned by Alembic (see migrations/). This module only checks
DB connectivity on startup and exposes HTTP endpoints.
"""

from contextlib import asynccontextmanager
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import engine, get_db
from app.models import Event, Span, Trace
from app.schemas import (
    EventBatchCreate,
    EventCreate,
    EventRead,
    SpanCreate,
    SpanRead,
    TraceDetail,
    TraceIngest,
    TraceListItem,
    TraceListResponse,
    TraceRead,
)


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


def _spans_in_parent_order(spans: list[SpanCreate]) -> list[SpanCreate]:
    """Parents before children so self-FK inserts succeed statement-by-statement."""
    by_id = {s.id: s for s in spans}
    remaining = set(by_id)
    ordered: list[SpanCreate] = []
    while remaining:
        ready = [
            sid
            for sid in remaining
            if by_id[sid].parent_span_id is None
            or by_id[sid].parent_span_id not in remaining
        ]
        for sid in ready:
            ordered.append(by_id[sid])
            remaining.remove(sid)
    return ordered


def _duration_ms(
    start: datetime | None,
    end: datetime | None,
    latency_sum: int | None,
) -> int | None:
    if start is not None and end is not None:
        return max(0, int((end - start).total_seconds() * 1000))
    return latency_sum


@app.post("/v1/traces", response_model=TraceRead, status_code=201)
async def create_trace(
    body: TraceIngest,
    db: AsyncSession = Depends(get_db),
):
    """Ingest one trace + nested spans atomically (ADR 0004)."""
    t = body.trace
    trace_row = Trace(
        id=t.id,
        name=t.name,
        status=t.status,
        start_time=t.start_time,
        end_time=t.end_time,
        meta=t.metadata,
    )
    db.add(trace_row)

    for s in _spans_in_parent_order(body.spans):
        db.add(
            Span(
                id=s.id,
                trace_id=t.id,
                parent_span_id=s.parent_span_id,
                name=s.name,
                provider=s.provider,
                model=s.model,
                input=s.input,
                output=s.output,
                prompt_tokens=s.prompt_tokens,
                completion_tokens=s.completion_tokens,
                total_tokens=s.total_tokens,
                latency_ms=s.latency_ms,
                cost_usd=s.cost_usd,
                status=s.status,
                start_time=s.start_time,
                end_time=s.end_time,
            )
        )

    await db.commit()
    await db.refresh(trace_row)
    return TraceRead.from_orm_trace(trace_row, span_count=len(body.spans))


@app.get("/v1/traces", response_model=TraceListResponse)
async def list_traces(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """Paginated traces, newest first, with span roll-ups (one aggregating query)."""
    total = await db.scalar(select(func.count()).select_from(Trace)) or 0

    # LEFT JOIN + GROUP BY → no N+1 (one round-trip for the page)
    agg = (
        select(
            Trace.id,
            Trace.name,
            Trace.status,
            Trace.start_time,
            Trace.end_time,
            Trace.created_at,
            func.count(Span.id).label("span_count"),
            func.coalesce(func.sum(Span.total_tokens), 0).label("total_tokens"),
            func.sum(Span.cost_usd).label("total_cost_usd"),
            func.coalesce(func.sum(Span.latency_ms), 0).label("latency_sum"),
        )
        .outerjoin(Span, Span.trace_id == Trace.id)
        .group_by(Trace.id)
        .order_by(Trace.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    rows = (await db.execute(agg)).all()

    items = [
        TraceListItem(
            id=r.id,
            name=r.name,
            status=r.status,
            start_time=r.start_time,
            end_time=r.end_time,
            created_at=r.created_at,
            span_count=int(r.span_count),
            total_tokens=int(r.total_tokens) if r.total_tokens is not None else None,
            total_cost_usd=r.total_cost_usd,
            duration_ms=_duration_ms(r.start_time, r.end_time, int(r.latency_sum)),
        )
        for r in rows
    ]
    return TraceListResponse(items=items, total=int(total), limit=limit, offset=offset)


@app.get("/v1/traces/{trace_id}", response_model=TraceDetail)
async def get_trace(
    trace_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Trace + flat span list (ADR 0005)."""
    result = await db.execute(select(Trace).where(Trace.id == trace_id))
    trace_row = result.scalar_one_or_none()
    if trace_row is None:
        raise HTTPException(status_code=404, detail="trace not found")

    spans_result = await db.execute(
        select(Span).where(Span.trace_id == trace_id).order_by(Span.start_time.asc())
    )
    spans = list(spans_result.scalars().all())

    token_sum = sum(s.total_tokens or 0 for s in spans) or None
    cost_vals = [s.cost_usd for s in spans if s.cost_usd is not None]
    cost_sum: Decimal | None = sum(cost_vals, Decimal("0")) if cost_vals else None
    latency_sum = sum(s.latency_ms or 0 for s in spans) or None

    return TraceDetail(
        id=trace_row.id,
        name=trace_row.name,
        status=trace_row.status,
        start_time=trace_row.start_time,
        end_time=trace_row.end_time,
        metadata=trace_row.meta,
        created_at=trace_row.created_at,
        span_count=len(spans),
        total_tokens=token_sum,
        total_cost_usd=cost_sum,
        duration_ms=_duration_ms(trace_row.start_time, trace_row.end_time, latency_sum),
        spans=[SpanRead.model_validate(s) for s in spans],
    )
