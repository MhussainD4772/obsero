# Changelog

Format based on [Keep a Changelog](https://keepachangelog.com/).  
Versions follow [SemVer](https://semver.org/).

**Habit:** one line per meaningful change under `[Unreleased]`.  
When you release, move that work into a versioned section and start a fresh `[Unreleased]`.

## [Unreleased]

### Added

- `traces` and `spans` tables (nested observability schema) via Alembic `0003` (OB-11)
- ADR 0003: keep flat `events` alongside traces/spans for now (OB-11)
- `POST /v1/traces` nested ingest (client UUIDs, parent/cycle validation, atomic insert) (OB-12)
- ADR 0004: nested ingest on `/v1/traces`, leave `/events/batch` alone (OB-12)
- SDK `obsero.trace` / `obsero.span` with contextvars; flush to `POST /v1/traces` (OB-13)
- `GET /v1/traces` (paginated + roll-ups) and `GET /v1/traces/{id}` (flat spans) (OB-14)
- ADR 0005: trace detail returns flat spans; client builds the tree (OB-14)
- Dashboard trace list + nested detail view; events section retained (OB-15)

### Changed

- SDK: nested `trace`/`span` replace the old single-call `trace` CM (use `track()` for flat events) (OB-13)

### Fixed

## [0.1.0] - 2026-07-28

First public cut: ingest → Postgres → dashboard for real LLM calls.

### Added

- Monorepo Docker Compose scaffold: Postgres, FastAPI `/health`, Next.js (OB-1)
- GitHub Actions CI: frontend lint/format/types + backend ruff
- Async SQLAlchemy + `events` table (OB-2)
- `POST /events` and `GET /events` (newest first) (OB-3)
- Installable Python SDK: `obsero.track()` → HTTP ingest; configurable base URL (OB-4)
- Next.js events list (TanStack Query) + FastAPI CORS for `localhost:3000` (OB-5)
- Alembic migrations; initial `events` revision (OB-6)
- Nullable LLM fields on `events` + migration `0002`; API accepts and returns them (OB-7)
- SDK `obsero.trace` context manager + Gemini example; `track()` sends LLM fields (OB-8)
- ADR 0002: context manager for LLM instrumentation; Gemini first for free-tier learning (OB-8)
- SDK pricing table + `estimate_cost`; `trace` fills `cost_usd` (OB-9)
- SDK in-memory batch buffer (size/time flush) + fail-safe (never raises into host) (OB-9)
- `POST /events/batch` batch ingest endpoint (OB-9)
- Dashboard LLM columns (model, tokens, latency, cost) + expandable input/output (OB-10)
- `docs/future-work.md` parking lot for deferred ideas
- Product README and MIT license for the public repo

### Changed

- Postgres host port mapped to `5433` to avoid clash with local Postgres on `5432`
- App startup no longer calls `create_all`; schema applied via `alembic upgrade head` (OB-6)
- Dashboard UI: clean dark mode (zinc-950) + `motion`
- SDK `track()` buffers and flushes via `/events/batch` instead of one POST per call (OB-9)
- Compose frontend: anonymous volume for `/app/.next` so Docker does not poison host Next cache

### Fixed

- Events list Refresh ignored updates when the browser cached `GET /events` (OB-5)
- Prettier VS Code paths: use relative `frontend/` paths (`${workspaceFolder}` not expanded by the extension)

[Unreleased]: https://github.com/MhussainD4772/obsero/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/MhussainD4772/obsero/releases/tag/v0.1.0
