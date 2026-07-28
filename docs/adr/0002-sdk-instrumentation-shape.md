# ADR 0002: SDK uses a context manager to instrument LLM calls

- **Status:** Accepted
- **Date:** 2026-07-27
- **Supersedes:** N/A
- **Superseded by:** N/A

## Context

OB-8 needs to wrap a real LLM chat call and record input, output, model,
token counts, and latency into Obsero via the existing POST /events path.
We had to choose how to wrap the call: decorator vs context manager.
For cost while learning, the first real provider is Gemini (Google AI Studio
free tier), not OpenAI — the data model stays provider-agnostic.

## Decision

Use a **context manager** (`with obsero.trace(...):`) as the instrumentation
API for v1. Capture Gemini responses into the nullable LLM fields from OB-7.

## Alternatives considered

1. **Decorator** (`@obsero.trace`) — familiar, but awkward to pull model and
   messages out of `*args`/`kwargs` when only part of the function is the
   LLM call.
2. **Context manager** — call site is explicit; model/input passed in at the
   `with` line; natural fit for “start timer → call → stop → ship event.”

## Consequences

**Good**

- Clear what is being timed and recorded
- Easy to pass model and messages in
- Can add a thin decorator later that uses the same context manager inside

**Bad / tradeoffs**

- Slightly more verbose than a one-line decorator
- Ticket text said OpenAI; we use Gemini for free-tier learning and note that
  in this ADR
