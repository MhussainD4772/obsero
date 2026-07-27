"""Pydantic request/response shapes for /events.

Separate from the ORM model on purpose: API validation can evolve
independently of the DB. LLM fields are optional so old clients still work.
"""

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


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
