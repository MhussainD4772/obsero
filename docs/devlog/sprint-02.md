# Sprint 02

**Dates:** 2026-08-04 → _end_  
**Goal:** Nested traces / spans — schema, ingest, SDK, query API, dashboard

---

## Ticket: OB-11 — Schema: traces and spans tables

### What I built

- ADR 0003: keep flat `events` alongside new `traces` / `spans` (no migrate yet)
- ORM models `Trace` and `Span` (self-FK `parent_span_id`; `meta` → column `metadata`)
- Alembic `0003_create_traces_spans`: tables + indexes on `traces(start_time)` and `spans(trace_id)`
- FKs: `trace_id` → traces ON DELETE CASCADE; `parent_span_id` → spans ON DELETE SET NULL
- Verified upgrade on DB with existing events (event count unchanged)

### Why (key decisions)

_Fill in — keep events vs deprecate/migrate; CASCADE vs SET NULL on parent._

### What fought me

_Fill in —_

### What I learned

_Fill in — adjacency list; why `metadata` can’t be the Python attr name._

---

## Ticket: _next ticket key_

### What I built

_Same headings as above — copy this block per ticket._

### Why (key decisions)

_

### What fought me

_

### What I learned

_
