"""Nested trace/span capture via contextvars (OB-13).

obsero.trace("run") opens a Trace; nested obsero.span("step") attach to the
active parent automatically. On trace exit → enqueue POST /v1/traces.
Capture failures never raise into the host; user exceptions still propagate.
"""

from __future__ import annotations

import logging
import time
import uuid
from contextvars import ContextVar, Token
from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import TracebackType
from typing import Any

from obsero.client import enqueue_trace
from obsero.pricing import estimate_cost

_log = logging.getLogger("obsero")

# Task-local stack: correct under asyncio (thread-locals are not)
_active_trace: ContextVar["_TraceBuf | None"] = ContextVar(
    "obsero_active_trace", default=None
)
_active_span_id: ContextVar[uuid.UUID | None] = ContextVar(
    "obsero_active_span_id", default=None
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class _TraceBuf:
    """In-memory trace built while context managers are open."""

    id: uuid.UUID
    name: str
    start_time: datetime
    status: str = "ok"
    spans: list[dict[str, Any]] = field(default_factory=list)
    end_time: datetime | None = None


class trace:
    """Outer run — owns the span list flushed on exit."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._buf: _TraceBuf | None = None
        self._token: Token[_TraceBuf | None] | None = None
        self._start_mono: float | None = None

    def __enter__(self) -> trace:
        try:
            self._buf = _TraceBuf(
                id=uuid.uuid4(),
                name=self.name,
                start_time=_utc_now(),
            )
            self._token = _active_trace.set(self._buf)
            self._start_mono = time.perf_counter()
        except Exception as exc:  # noqa: BLE001
            _log.warning("trace enter failed: %s", exc)
            self._buf = None
            self._token = None
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        try:
            if self._buf is None:
                return None
            if exc is not None:
                self._buf.status = "error"
            self._buf.end_time = _utc_now()
            payload = {
                "trace": {
                    "id": str(self._buf.id),
                    "name": self._buf.name,
                    "status": self._buf.status,
                    "start_time": self._buf.start_time.isoformat(),
                    "end_time": self._buf.end_time.isoformat(),
                },
                "spans": list(self._buf.spans),
            }
            enqueue_trace(payload)
        except Exception as ship_exc:  # noqa: BLE001
            _log.warning("trace exit flush failed: %s", ship_exc)
        finally:
            if self._token is not None:
                try:
                    _active_trace.reset(self._token)
                except Exception:  # noqa: BLE001
                    pass
        # Never swallow the host's exception
        return None


class span:
    """One step inside an active trace (or no-op fail-safe if none)."""

    def __init__(
        self,
        name: str,
        *,
        model: str | None = None,
        input: dict[str, Any] | None = None,
        provider: str | None = None,
    ) -> None:
        self.name = name
        self.model = model
        self.input = input
        self.provider = provider
        self._id = uuid.uuid4()
        self._parent_id: uuid.UUID | None = None
        self._output: dict[str, Any] | None = None
        self._prompt_tokens: int | None = None
        self._completion_tokens: int | None = None
        self._total_tokens: int | None = None
        self._status = "ok"
        self._start_mono: float | None = None
        self._start_wall: datetime | None = None
        self._token: Token[uuid.UUID | None] | None = None
        self._attached = False

    def set_output(self, output: dict[str, Any]) -> None:
        self._output = output

    def set_usage(
        self,
        *,
        prompt_tokens: int | None = None,
        completion_tokens: int | None = None,
        total_tokens: int | None = None,
    ) -> None:
        self._prompt_tokens = prompt_tokens
        self._completion_tokens = completion_tokens
        self._total_tokens = total_tokens

    def set_status(self, status: str) -> None:
        self._status = status

    def __enter__(self) -> span:
        try:
            buf = _active_trace.get()
            if buf is None:
                _log.warning("span(%r) outside trace — not recorded", self.name)
                return self
            self._parent_id = _active_span_id.get()
            self._token = _active_span_id.set(self._id)
            self._start_mono = time.perf_counter()
            self._start_wall = _utc_now()
            self._attached = True
        except Exception as exc:  # noqa: BLE001
            _log.warning("span enter failed: %s", exc)
            self._attached = False
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        try:
            if not self._attached or self._start_mono is None:
                return None
            buf = _active_trace.get()
            if buf is None:
                return None
            if exc is not None:
                self._status = "error"
            end_wall = _utc_now()
            latency_ms = int((time.perf_counter() - self._start_mono) * 1000)
            cost = None
            if self.model is not None:
                cost = estimate_cost(
                    self.model,
                    self._prompt_tokens,
                    self._completion_tokens,
                )
            row: dict[str, Any] = {
                "id": str(self._id),
                "parent_span_id": str(self._parent_id)
                if self._parent_id is not None
                else None,
                "name": self.name,
                "status": self._status,
                "latency_ms": latency_ms,
                "start_time": self._start_wall.isoformat()
                if self._start_wall
                else None,
                "end_time": end_wall.isoformat(),
            }
            optional = {
                "provider": self.provider,
                "model": self.model,
                "input": self.input,
                "output": self._output,
                "prompt_tokens": self._prompt_tokens,
                "completion_tokens": self._completion_tokens,
                "total_tokens": self._total_tokens,
                "cost_usd": str(cost) if cost is not None else None,
            }
            row.update({k: v for k, v in optional.items() if v is not None})
            buf.spans.append(row)
        except Exception as record_exc:  # noqa: BLE001
            # Broken span must not discard the rest of the trace
            _log.warning("span exit record failed: %s", record_exc)
        finally:
            if self._token is not None:
                try:
                    _active_span_id.reset(self._token)
                except Exception:  # noqa: BLE001
                    pass
        return None
