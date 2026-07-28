import os
from typing import Any

import httpx

_base_url: str | None = None


def init(base_url: str | None = None) -> None:
    """Set the Obsero API base URL (no trailing slash)."""
    global _base_url
    _base_url = (
        base_url or os.getenv("OBSERO_BASE_URL", "http://localhost:8000")
    ).rstrip("/")


def _get_base_url() -> str:
    if _base_url is None:
        init()  # lazy default on first use
    assert _base_url is not None
    return _base_url


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
) -> dict[str, Any]:
    """POST an event to /events. Optional LLM fields match the OB-7 API."""
    url = f"{_get_base_url()}/events"
    body: dict[str, Any] = {"name": name, "payload": payload or {}}
    # Only send keys that were set — keeps payloads small for legacy callers
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
    with httpx.Client(timeout=10.0) as client:
        response = client.post(url, json=body)
        response.raise_for_status()
        return response.json()
