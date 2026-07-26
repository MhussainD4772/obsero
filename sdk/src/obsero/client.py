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


def track(name: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    """POST an event to /events. Returns the created event JSON."""
    url = f"{_get_base_url()}/events"
    body = {"name": name, "payload": payload or {}}
    with httpx.Client(timeout=10.0) as client:
        response = client.post(url, json=body)
        response.raise_for_status()
        return response.json()
