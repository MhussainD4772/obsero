# ADR 0003: Keep flat `events` alongside new `traces` / `spans`

- **Status:** Accepted
- **Date:** 2026-08-04
- **Supersedes:** N/A
- **Superseded by:** N/A

## Context

OB-11 adds nested observability tables (`traces`, `spans`). The v0.1 product
already has a flat `events` table, a working SDK `track()` / `trace` path, and
a dashboard that reads `GET /events`. We must decide whether to keep, deprecate,
or migrate that table while introducing the tree model.

## Decision

**Keep `events` alongside `traces` / `spans` for now.**  
OB-11 only adds the new tables (additive Alembic migration). Existing event
rows and the current ingest/UI stay unchanged. Deprecation or backfill into
spans is deferred until the trace ingest API and dashboard (OB-12+) are live.

## Alternatives considered

1. **Keep alongside (chosen)** — zero risk to v0.1; clear cutover later.
2. **Deprecate immediately** (keep table, stop writing) — forces dual paths
   before the new API exists; dashboard would break without a rewrite.
3. **Migrate existing rows into spans** — flat events have no real parent tree;
   a synthetic one-span-per-event migration is possible but low value and easy
   to get wrong under time pressure.

## Consequences

**Good**

- Existing data and dashboard keep working through the schema change
- Migration is additive and easy to verify (`events` count unchanged)
- Trace work can ship independently of the flat-event path

**Bad / tradeoffs**

- Two persistence models until a later cutover ticket
- Risk of dual-write confusion if we don’t document which path is “new”
  (new work writes traces; legacy path still writes events)
