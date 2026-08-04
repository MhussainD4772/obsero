# ADR 0005: Trace detail returns a flat span list

- **Status:** Accepted
- **Date:** 2026-08-04
- **Supersedes:** N/A
- **Superseded by:** N/A

## Context

OB-14's `GET /v1/traces/{id}` must return a trace plus its span tree.
Two shapes: nest children in JSON, or return a flat list with
`parent_span_id` and let the client assemble the tree.

## Decision

Return a **flat list of spans** (adjacency list). The dashboard (OB-15)
builds the tree in TypeScript for indentation.

## Alternatives considered

1. **Pre-nested JSON** — convenient for simple UIs, but recursive schemas
   are awkward in OpenAPI/Pydantic and harder to paginate later.
2. **Flat list (chosen)** — one query, stable schema, matches how we store
   rows; tree assembly is a small client helper.

## Consequences

**Good**

- Simple SQL (`WHERE trace_id = …`)
- Dashboard controls depth/collapse without re-fetching shape

**Bad / tradeoffs**

- Every client must know how to build a tree from parent pointers
