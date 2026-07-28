"""Obsero SDK — track events to the Obsero backend."""

from obsero.client import init, track
from obsero.trace import trace

__version__ = "0.1.0"
__all__ = ["init", "track", "trace", "__version__"]
