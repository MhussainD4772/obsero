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

## Ticket: OB-12 — Ingest API: accept a trace with nested spans

### What I built

- ADR 0004: new `POST /v1/traces` (not extending `/events/batch`)
- Pydantic `TraceIngest`: client UUIDs; reject duplicate ids, missing parents, cycles
- Endpoint inserts trace + spans in one transaction; response includes `span_count`
- Spans inserted parent-before-child for self-FK safety

### Why (key decisions)

_Fill in — client UUIDs; why not extend batch; idempotency thoughts._

### What fought me

_Fill in —_

### What I learned

_Fill in — tree validation in Pydantic; transactional all-or-nothing._

---

## Ticket: OB-13 — SDK: nested span capture

### What I built

- `obsero.trace` / `obsero.span` context managers with contextvars for parent stack
- Client UUIDs; exception → span `status=error`, host exception still propagates
- `enqueue_trace` + flush to `POST /v1/traces`; fail-safe logging
- Examples: `nested_trace_demo.py`, updated `gemini_chat.py`

### Why (key decisions)

_Fill in — contextvars; rename old LLM-only trace._

### What fought me

_Fill in —_

### What I learned

_Fill in —_

---

## Ticket: OB-14 — Query API: trace list and detail

### What I built

- `GET /v1/traces` paginated list with SQL roll-ups (spans, tokens, cost, duration)
- `GET /v1/traces/{id}` with flat span list
- ADR 0005: flat vs nested response tradeoff

### Why (key decisions)

_Fill in — flat spans; offset pagination._

### What fought me

_Fill in —_

### What I learned

_Fill in —_

---

## Ticket: OB-15 — Dashboard: trace list and nested detail

### What I built

- Home: traces table (roll-ups) + retained events section
- `/traces/[id]`: roll-up cards + indented span tree with I/O expand
- Client `buildSpanTree` / `flattenSpanTree` from flat API

### Why (key decisions)

_Fill in —_

### What fought me

_Fill in —_

### What I learned

_Fill in —_

