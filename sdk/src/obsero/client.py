"""HTTP client for Obsero events + nested traces.

track() → POST /events/batch; enqueue_trace() → POST /v1/traces.
Never raises into the host app.
"""

from __future__ import annotations

import atexit
import logging
import os
import threading
from typing import Any

import httpx

_log = logging.getLogger("obsero")

_base_url: str | None = None
_buffer: list[dict[str, Any]] = []
_trace_buffer: list[dict[str, Any]] = []
_lock = threading.Lock()
_timer: threading.Timer | None = None

_FLUSH_SIZE = 10
_FLUSH_INTERVAL_S = 2.0


def init(base_url: str | None = None) -> None:
    """Set the Obsero API base URL (no trailing slash)."""
    global _base_url
    _base_url = (
        base_url or os.getenv("OBSERO_BASE_URL", "http://localhost:8000")
    ).rstrip("/")


def _get_base_url() -> str:
    if _base_url is None:
        init()
    assert _base_url is not None
    return _base_url


def _schedule_flush() -> None:
    """Ensure a timer will flush; reset if one was already running."""
    global _timer
    if _timer is not None:
        _timer.cancel()
    _timer = threading.Timer(_FLUSH_INTERVAL_S, flush)
    _timer.daemon = True
    _timer.start()


def flush() -> None:
    """Send buffered events and traces. Safe anytime; never raises."""
    global _timer
    with _lock:
        if _timer is not None:
            _timer.cancel()
            _timer = None
        events = list(_buffer)
        traces = list(_trace_buffer)
        _buffer.clear()
        _trace_buffer.clear()

    if events:
        try:
            url = f"{_get_base_url()}/events/batch"
            with httpx.Client(timeout=10.0) as client:
                response = client.post(url, json={"events": events})
                response.raise_for_status()
        except Exception as exc:  # noqa: BLE001
            _log.warning("event flush failed (%d dropped): %s", len(events), exc)

    # One POST per completed tree (matches POST /v1/traces contract)
    for payload in traces:
        try:
            url = f"{_get_base_url()}/v1/traces"
            with httpx.Client(timeout=10.0) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
        except Exception as exc:  # noqa: BLE001
            _log.warning("trace flush failed: %s", exc)


def enqueue_trace(payload: dict[str, Any]) -> None:
    """Queue a finished trace+spans payload; flush on size or timer."""
    should_flush = False
    with _lock:
        _trace_buffer.append(payload)
        if len(_trace_buffer) + len(_buffer) >= _FLUSH_SIZE:
            should_flush = True
        else:
            _schedule_flush()
    if should_flush:
        flush()


def track(
    name: str,
    payload: dict[str, Any] | None = None,
    *,
    provider: str | None = None,
    model: str | None = None,
    input: dict[str, Any] | None = None,
    output: dict[str, Any] | None = None,
    prompt_tokens: int | None = None,
    completion_tokens: int | None = None,
    total_tokens: int | None = None,
    latency_ms: int | None = None,
    cost_usd: float | str | None = None,
    status: str | None = None,
) -> None:
    """Queue a flat event; flush on size or time. Never raises into the host."""
    body: dict[str, Any] = {"name": name, "payload": payload or {}}
    optional = {
        "provider": provider,
        "model": model,
        "input": input,
        "output": output,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "latency_ms": latency_ms,
        "cost_usd": cost_usd,
        "status": status,
    }
    body.update({k: v for k, v in optional.items() if v is not None})

    should_flush = False
    with _lock:
        _buffer.append(body)
        if len(_buffer) >= _FLUSH_SIZE:
            should_flush = True
        else:
            _schedule_flush()

    if should_flush:
        flush()


atexit.register(flush)
