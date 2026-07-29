"""Context manager that times an LLM call and ships an Obsero event.

Usage:
    with obsero.trace(name="chat", model="gemini-2.0-flash", input={...}) as span:
        # call Gemini yourself; then:
        span.set_output({"text": "..."})
        span.set_usage(prompt_tokens=..., completion_tokens=..., total_tokens=...)
    # on exit → track() with latency_ms
"""

from __future__ import annotations

import time
from types import TracebackType
from typing import Any

from obsero.client import track
from obsero.pricing import estimate_cost


class trace:
    """Instrument one LLM call. Provider defaults to google (Gemini first)."""

    def __init__(
        self,
        name: str,
        *,
        model: str,
        input: dict[str, Any] | None = None,
        provider: str = "google",
    ) -> None:
        self.name = name
        self.model = model
        self.input = input
        self.provider = provider
        self._output: dict[str, Any] | None = None
        self._prompt_tokens: int | None = None
        self._completion_tokens: int | None = None
        self._total_tokens: int | None = None
        self._status = "ok"
        self._start: float | None = None

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

    def __enter__(self) -> trace:
        self._start = time.perf_counter()  # monotonic clock for durations
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        assert self._start is not None
        latency_ms = int((time.perf_counter() - self._start) * 1000)
        if exc is not None:
            self._status = "error"
        cost = estimate_cost(
            self.model,
            self._prompt_tokens,
            self._completion_tokens,
        )
        track(
            self.name,
            provider=self.provider,
            model=self.model,
            input=self.input,
            output=self._output,
            prompt_tokens=self._prompt_tokens,
            completion_tokens=self._completion_tokens,
            total_tokens=self._total_tokens,
            latency_ms=latency_ms,
            cost_usd=str(cost) if cost is not None else None,
            status=self._status,
        )
        # return None → don't swallow the exception; host still sees it
        return None
