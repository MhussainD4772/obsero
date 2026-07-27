"""Add nullable LLM call columns to events.

Revision ID: 0002_add_llm_fields
Revises: 0001_create_events
Create Date: 2026-07-27

Backward-compatible: all new columns are nullable so Sprint 1 rows survive.
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0002_add_llm_fields"
down_revision: Union[str, None] = "0001_create_events"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("events", sa.Column("provider", sa.String(length=64), nullable=True))
    op.add_column("events", sa.Column("model", sa.String(length=128), nullable=True))
    op.add_column(
        "events",
        sa.Column("input", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.add_column(
        "events",
        sa.Column("output", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.add_column("events", sa.Column("prompt_tokens", sa.Integer(), nullable=True))
    op.add_column("events", sa.Column("completion_tokens", sa.Integer(), nullable=True))
    op.add_column("events", sa.Column("total_tokens", sa.Integer(), nullable=True))
    op.add_column("events", sa.Column("latency_ms", sa.Integer(), nullable=True))
    op.add_column(
        "events",
        sa.Column("cost_usd", sa.Numeric(precision=12, scale=6), nullable=True),
    )
    op.add_column("events", sa.Column("status", sa.String(length=32), nullable=True))


def downgrade() -> None:
    op.drop_column("events", "status")
    op.drop_column("events", "cost_usd")
    op.drop_column("events", "latency_ms")
    op.drop_column("events", "total_tokens")
    op.drop_column("events", "completion_tokens")
    op.drop_column("events", "prompt_tokens")
    op.drop_column("events", "output")
    op.drop_column("events", "input")
    op.drop_column("events", "model")
    op.drop_column("events", "provider")
