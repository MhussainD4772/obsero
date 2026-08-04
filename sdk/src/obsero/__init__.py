"""Obsero SDK — flat events + nested traces/spans."""

from obsero.client import flush, init, track
from obsero.tracing import span, trace

__version__ = "0.2.0"
__all__ = ["flush", "init", "track", "trace", "span", "__version__"]
