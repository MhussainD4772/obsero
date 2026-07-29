# Sprint 01

**Dates:** 2026-07-21 → _end_  
**Goal:** … LLM fields on events (OB-7), SDK Gemini capture via context manager (OB-8)

---

## Ticket: OB-1 — Repo + Docker Compose scaffold

### What I built

- Monorepo folders: `backend/`, `frontend/`, `sdk/`
- Root `docker-compose.yml` with `postgres`, `backend`, `frontend` (dev bind-mounts + hot reload)
- FastAPI stub: `GET /health` → `{"status":"ok"}` at `localhost:8000`
- Next.js App Router scaffold (`create-next-app`) at `localhost:3000`
- Dockerfiles for backend (Python/Uvicorn) and frontend (Node/`next dev`)
- Formatter setup: Prettier (frontend) + Ruff (backend) + format-on-save

### Why (key decisions)

_Fill in your words — e.g. why dev Compose + bind mounts vs prod-style rebuilds; why create-next-app for Next but hand-write FastAPI /health._

### What fought me

_Fill in — e.g. Compose YAML indentation, port 3000 already allocated, frontend container without published ports until --force-recreate, Docker build context size / node_modules._

### What I learned

_Fill in — one or two concrete takeaways (service DNS vs localhost, anonymous volume for node_modules, etc.)._

---

## Ticket: OB-2 — FastAPI: DB connection + events table

### What I built

- Backend deps: SQLAlchemy asyncio, asyncpg, pydantic-settings
- `app/db.py` — async engine, session factory, `get_db`, `DATABASE_URL`
- `app/models.py` — `Event` ORM model (`id`, `name`, `payload` JSONB, `created_at`)
- `app/schemas.py` — Pydantic `EventCreate` / `EventRead`
- Startup lifespan: `SELECT 1` + `create_all` (fail loudly if DB down)
- Compose: `DATABASE_URL` env; host Postgres published on **5433** (avoids local Postgres on 5432)
- Local `backend/.venv` + VS Code interpreter path for IDE imports

### Why (key decisions)

_Fill in — e.g. create_all vs Alembic for now; why host port 5433; async SQLAlchemy._

### What fought me

_Fill in — e.g. Pylance “sqlalchemy could not be resolved”, TablePlus hitting local Postgres on 5432, leftover applications_tracker on 5433._

### What I learned

_Fill in — service DNS vs localhost for DB tools; roles/ports; lifespan startup._

---

## Ticket: OB-3 — FastAPI: POST /events and GET /events

### What I built

- `POST /events` — body `EventCreate`, insert via `get_db`, return `EventRead` with `201`
- `GET /events` — list all events, newest first (`created_at.desc()`)
- Verified with curl: POST creates row with `id` + `created_at`; GET returns JSON array

### Why (key decisions)

_Fill in — e.g. Depends(get_db), response_model, 201 vs 200, order newest-first._

### What fought me

_Fill in — anything that slowed you down on this ticket._

### What I learned

_Fill in — commit/refresh, Pydantic ↔ ORM, select/order_by._

---

## Ticket: OB-4 — SDK: minimal obsero package

### What I built

- Installable package under `sdk/` (`pyproject.toml` + `src/obsero/` hatchling layout)
- `pip install -e ./sdk` → `import obsero`
- `obsero.init()` / env `OBSERO_BASE_URL` (default `http://localhost:8000`)
- `obsero.track(name, payload)` POSTs to `/events` via httpx; returns created event JSON
- Verified: track creates a visible row (`id`, `name`, `payload`, `created_at`)

### Why (key decisions)

_Fill in — e.g. src layout vs flat; httpx; init + env vs env-only; module-level base URL._

### What fought me

_Fill in — e.g. duplicate TOML dependencies keys, unsaved client.py on disk, zsh quoting / no bare `python` without venv._

### What I learned

_Fill in — editable installs, package exports in `__init__`, client vs API contract._

---

## Ticket: OB-5 — Next.js: events list page

### What I built

- FastAPI CORS middleware allowing `http://localhost:3000`
- TanStack Query provider + `fetchEvents()` client (`cache: "no-store"`)
- Brutalist off-white events table (name, payload, timestamp) with Refresh
  _(UI later moved to clean dark mode — see CHANGELOG)_
- Replaced temporary GIF home page; DoD: SDK `track()` → Refresh → new row

### Why (key decisions)

_Fill in — e.g. client fetch + TanStack vs server component; CORS origin lock; no-store cache._

### What fought me

_Fill in — e.g. browser caching GET /events making Refresh look broken._

### What I learned

_Fill in — CORS vs curl/SDK, QueryClientProvider, refetch vs cache._

---

## Ticket: OB-6 — Introduce Alembic and take over schema management

### What I built

- Alembic (async) under `backend/migrations/` + `alembic.ini`
- Initial revision `0001_create_events` matching the current `events` table
- Removed `create_all` from app lifespan; kept `SELECT 1` connectivity check
- `entrypoint.sh` runs `alembic upgrade head` before Uvicorn; Compose uses it
- Verified: fresh DB + `upgrade head` produces the expected `events` schema

### Why (key decisions)

_Fill in — e.g. why migrations folder not named alembic/; stamp vs upgrade on existing DB; migrate in entrypoint vs manual only._

### What fought me

_Fill in — e.g. local `alembic/` package shadow, Docker rebuild stuck, stamp for create_all-era DBs._

### What I learned

_Fill in — alembic_version, upgrade vs stamp, create_all cannot alter tables._

---

## Ticket: OB-7 — Extend the data model to a real LLM call

### What I built

- Nullable LLM columns on `Event` ORM: provider, model, input/output JSONB, token counts, latency_ms, cost_usd (Numeric), status
- Alembic revision `0002_add_llm_fields_to_events` (autogenerate via Docker; renamed from hash id)
- `EventCreate` / `EventRead` extended; `POST /events` persists all fields; `GET` returns them
- Old Sprint 1 rows survive (null LLM fields); full LLM POST round-trip verified
- Frontend `Event` type updated with optional LLM fields (UI columns deferred to OB-10)

### Why (key decisions)

_Fill in — nullable columns for backward compat; Numeric for cost; keep payload alongside input/output._

### What fought me

_Fill in — SQLAlchemy 3.14 host venv vs Docker 3.11 for autogenerate; run alembic in container._

### What I learned

_Fill in — first additive migration after OB-6; API schema optional fields vs DB nullable._

---

## Ticket: OB-8 — SDK: capture a real LLM call (Gemini)

### What I built

- ADR 0002: context manager over decorator; Gemini (free tier) as first real provider
- `track()` accepts optional LLM fields (provider, model, tokens, latency, etc.)
- `obsero.trace` context manager: `perf_counter` latency, `set_output` / `set_usage`, ships via `track()`
- `google-genai` dependency; example `sdk/examples/gemini_chat.py` (model `gemini-flash-latest`)
- Verified: real Gemini call → row with prompt/completion/total tokens + latency_ms

### Why (key decisions)

_Fill in — context manager vs decorator; Gemini vs OpenAI for learning cost; gemini-flash-latest alias._

### What fought me

_Fill in — 429/404 on retired model ids; list models for the key; remember to source .env._

### What I learned

_Fill in — usage_metadata; perf_counter; provider default is overrideable._

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
