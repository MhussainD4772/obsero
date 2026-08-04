# Obsero

[![CI](https://github.com/MhussainD4772/obsero/actions/workflows/ci.yml/badge.svg)](https://github.com/MhussainD4772/obsero/actions/workflows/ci.yml)

**Open-source, self-hostable observability for LLM applications.**

## What is Obsero?

LLM features often hide cost, latency, and quality behind provider APIs. Obsero is a self-hosted stack that records those calls and shows them in a dashboard.

You wrap existing LLM calls with a small Python SDK. Obsero stores prompt, response, model, tokens, latency, and estimated cost in Postgres, then lists them in a Next.js UI — on infrastructure you run.

## Status — v0.1.0 (early)

**Works today**

- Python SDK: `track()` and `trace` context manager
- Capture of real Gemini calls (example script); fields match a generic LLM event shape
- FastAPI ingest: `POST /events`, `POST /events/batch`, `GET /events`
- Postgres schema via Alembic
- Per-model cost estimate with fallback for unknown models
- In-memory SDK batching + fail-safe flush (backend down does not crash the host app)
- Dashboard: model, tokens, latency, cost; expand a row for input/output

**Not in v0.1.0**

- Auth / multi-project tenancy
- Nested traces / spans
- Cost or latency analytics charts
- Datasets or LLM-as-judge evals

## Quickstart

### Requirements

- Docker Compose
- Node 22+ (if you run the dashboard on the host)
- Python 3.11+ (SDK / example)
- Optional: a Gemini API key for the example script

### 1. Clone and start API + database

```bash
git clone https://github.com/MhussainD4772/obsero.git
cd obsero
docker compose up -d postgres backend
```

The backend entrypoint runs `alembic upgrade head`, then serves the API.

| Service | Where |
|---------|--------|
| API | http://localhost:8000 (`/health`, `/events`) |
| Postgres | host port **5433** → container `5432` (user / password / db: `obsero`) |

Compose also defines a `frontend` service on port 3000. For day-to-day UI work, prefer a host Next process (below) so Docker and local Turbopack do not share a conflicting `.next` cache.

### 2. Environment variables

| Variable | Who | Required? | Notes |
|----------|-----|-----------|--------|
| `DATABASE_URL` | backend | Set in Compose | `postgresql+asyncpg://obsero:obsero@postgres:5432/obsero` |
| `OBSERO_BASE_URL` | SDK | No | Defaults to `http://localhost:8000` |
| `NEXT_PUBLIC_API_URL` | frontend | No | Defaults to `http://localhost:8000` |
| `GEMINI_API_KEY` | Gemini example only | For the example | Put in a repo-root `.env` (gitignored) and load before running the script |

Example repo-root `.env` (do not commit secrets):

```bash
GEMINI_API_KEY=your_key_here
# OBSERO_BASE_URL=http://localhost:8000
```

### 3. Dashboard (host)

```bash
cd frontend
npm ci
npm run dev
```

Open http://localhost:3000

### 4. Install the SDK and send a test event

```bash
# from repo root, in a venv
pip install -e ./sdk
python -c "import obsero; obsero.track('hello', {'ok': True}); obsero.flush()"
```

Refresh the dashboard.

### 5. Optional — real Gemini call

```bash
set -a && source .env && set +a
python sdk/examples/gemini_chat.py
```

Uses nested `obsero.trace` / `obsero.span` and model `gemini-flash-latest`.
Flushes to `POST /v1/traces`. Refresh the UI — one trace row, click for the span tree.

### 6. Optional — nested demo (no API key)

```bash
python sdk/examples/nested_trace_demo.py
```

## How it works

**In your app:** wrap a run in `obsero.trace(...)` and steps in `obsero.span(...)`.
Parent links use contextvars (async-safe). On exit the SDK POSTs the tree to
`/v1/traces`. Flat `track()` still ships to `/events/batch`. Capture failures
are logged; they do not raise into your app.

**As a system you host:** Compose runs Postgres and FastAPI. The dashboard lists
`GET /v1/traces` and detail at `/traces/[id]` (flat spans → client tree). Legacy
events remain on the home page.

```
Your application
      │
      │  obsero.trace / span  ·  obsero.track
      ▼
Python SDK (httpx) ──POST /v1/traces──────────► FastAPI
                   ──POST /events/batch───────►    │
                                                   ▼
                                              PostgreSQL
                                                   │
Browser ◄──── GET /v1/traces · /events ◄──────────┘
(Next.js dashboard)
```

## Tech stack

| Layer | Technology |
|-------|------------|
| SDK | Python, httpx (`google-genai` for the Gemini example) |
| Backend | FastAPI, async SQLAlchemy, Pydantic v2, Alembic |
| Database | PostgreSQL 16 |
| Dashboard | Next.js (App Router), TypeScript, Tailwind, TanStack Query |
| Infra | Docker Compose |

## Roadmap

Toward a fuller v1 product:

- Nested traces / spans for multi-step agents
- Cost and latency analytics
- Datasets + LLM-as-judge evaluation
- Auth and projects
- Hardened one-command self-host

## Contributing

Obsero is open source. Issues and pull requests are welcome.

Keep changes focused, match the existing stack, and open an issue before large features so direction stays aligned. `main` is protected; PRs need green CI.

## License

MIT — see [`LICENSE`](LICENSE).
