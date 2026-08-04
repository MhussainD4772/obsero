# ADR 0004: Nested trace ingest via POST /v1/traces

- **Status:** Accepted
- **Date:** 2026-08-04
- **Supersedes:** N/A
- **Superseded by:** N/A

## Context

OB-12 needs an HTTP path that accepts one trace plus its span tree in a
single request (client-generated UUIDs, parent links, atomic insert).
We already have `POST /events/batch` for flat v0.1 events.

## Decision

Add **`POST /v1/traces`** for nested ingest. Leave `/events` and
`/events/batch` unchanged for the flat SDK/dashboard path (ADR 0003).

## Alternatives considered

1. **Extend `/events/batch`** — one URL for everything, but mixes two
   payload shapes and risks breaking the existing SDK flush contract.
2. **New `/v1/traces` (chosen)** — clear versioned surface for the tree
   model; flat and nested APIs evolve independently.

## Consequences

**Good**

- No breakage of current `track()` / batch flush
- Room to version nested APIs under `/v1/` as tracing grows

**Bad / tradeoffs**

- Two ingest entry points until events are deprecated
- SDK (OB-13) must call the new path for nested traces
