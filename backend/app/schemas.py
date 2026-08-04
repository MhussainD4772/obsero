"""Pydantic request/response shapes for events + nested traces.

Separate from the ORM on purpose: API validation can evolve independently
of the DB. Trace ingest validates the span tree before any insert (OB-12).
"""

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class EventCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    payload: dict = Field(default_factory=dict)

    # LLM fields — all optional (omit or null for generic events)
    provider: str | None = None
    model: str | None = None
    input: dict | None = None
    output: dict | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    latency_ms: int | None = None
    cost_usd: Decimal | None = None
    status: str | None = None


class EventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    payload: dict
    created_at: datetime

    provider: str | None = None
    model: str | None = None
    input: dict | None = None
    output: dict | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    latency_ms: int | None = None
    cost_usd: Decimal | None = None
    status: str | None = None


class EventBatchCreate(BaseModel):
    events: list[EventCreate] = Field(min_length=1, max_length=100)


# --- Nested traces (OB-12): client supplies UUIDs so parents can link ---


class TraceCreate(BaseModel):
    id: uuid.UUID
    name: str = Field(min_length=1, max_length=255)
    status: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    metadata: dict | None = None


class SpanCreate(BaseModel):
    id: uuid.UUID
    parent_span_id: uuid.UUID | None = None
    name: str = Field(min_length=1, max_length=255)
    provider: str | None = None
    model: str | None = None
    input: dict | None = None
    output: dict | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    latency_ms: int | None = None
    cost_usd: Decimal | None = None
    status: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None


class TraceIngest(BaseModel):
    """One trace + its spans in a single request."""

    trace: TraceCreate
    spans: list[SpanCreate] = Field(default_factory=list, max_length=500)

    @model_validator(mode="after")
    def validate_span_tree(self) -> "TraceIngest":
        ids = [s.id for s in self.spans]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate span id in payload")

        id_set = set(ids)
        parents: dict[uuid.UUID, uuid.UUID | None] = {
            s.id: s.parent_span_id for s in self.spans
        }

        for span in self.spans:
            parent = span.parent_span_id
            if parent is None:
                continue
            if parent not in id_set:
                raise ValueError(
                    f"parent_span_id {parent} not present in payload (span {span.id})"
                )
            if parent == span.id:
                raise ValueError(f"span {span.id} cannot be its own parent")

        # Cycle check: walk each node's ancestors; revisit on one path = cycle
        for start in id_set:
            seen: set[uuid.UUID] = set()
            current: uuid.UUID | None = start
            while current is not None:
                if current in seen:
                    raise ValueError("cycle detected in span tree")
                seen.add(current)
                current = parents.get(current)

        return self


class TraceRead(BaseModel):
    """Response after ingest — ORM uses `meta`, API exposes `metadata`."""

    id: uuid.UUID
    name: str
    status: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    metadata: dict | None = None
    created_at: datetime
    span_count: int

    @classmethod
    def from_orm_trace(cls, trace: object, span_count: int) -> "TraceRead":
        return cls(
            id=trace.id,  # type: ignore[attr-defined]
            name=trace.name,  # type: ignore[attr-defined]
            status=trace.status,  # type: ignore[attr-defined]
            start_time=trace.start_time,  # type: ignore[attr-defined]
            end_time=trace.end_time,  # type: ignore[attr-defined]
            metadata=trace.meta,  # type: ignore[attr-defined]
            created_at=trace.created_at,  # type: ignore[attr-defined]
            span_count=span_count,
        )


# --- Query API (OB-14) ---


class TraceListItem(BaseModel):
    """One row in GET /v1/traces with roll-ups from spans."""

    id: uuid.UUID
    name: str
    status: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    created_at: datetime
    span_count: int
    total_tokens: int | None = None
    total_cost_usd: Decimal | None = None
    # Prefer wall-clock duration when start/end set; else sum of span latency_ms
    duration_ms: int | None = None


class TraceListResponse(BaseModel):
    items: list[TraceListItem]
    total: int
    limit: int
    offset: int


class SpanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    trace_id: uuid.UUID
    parent_span_id: uuid.UUID | None = None
    name: str
    provider: str | None = None
    model: str | None = None
    input: dict | None = None
    output: dict | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    latency_ms: int | None = None
    cost_usd: Decimal | None = None
    status: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None


class TraceDetail(BaseModel):
    """GET /v1/traces/{id} — flat span list; client builds the tree (ADR 0005)."""

    id: uuid.UUID
    name: str
    status: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    metadata: dict | None = None
    created_at: datetime
    span_count: int
    total_tokens: int | None = None
    total_cost_usd: Decimal | None = None
    duration_ms: int | None = None
    spans: list[SpanRead]
