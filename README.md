# Obsero

[![CI](https://github.com/MhussainD4772/obsero/actions/workflows/ci.yml/badge.svg)](https://github.com/MhussainD4772/obsero/actions/workflows/ci.yml)

**Self-hostable observability for LLM applications.**

Obsero captures prompts, responses, tokens, latency, and cost from your LLM calls, stores them in Postgres, and shows them in a dashboard — so you can see what your AI features are actually doing.

> **Status:** early development. The ingest → store → dashboard path works today. Nested traces, analytics charts, evals, and multi-project auth are on the roadmap.

---

## Why Obsero?

Building with LLMs without instrumentation is flying blind: slow prompts, surprise bills, and silent quality regressions after a model or prompt change.

Obsero is built to be:

- **Self-hosted** — one Compose stack; your data stays yours
- **SDK-first** — wrap existing calls; don’t rewrite your app
- **Honest about cost** — token usage in, estimated USD out
- **Fail-safe** — if the backend is down, your app keeps running

---

## What’s working now

| Area | Capability |
|------|------------|
| **Ingest** | Python SDK `track()` and `trace` context manager |
| **Providers** | Real Gemini capture example (OpenAI-shaped fields work the same path) |
| **API** | `POST /events`, `POST /events/batch`, `GET /events` |
| **Storage** | Postgres + Alembic migrations |
| **Cost** | Per-model pricing table + fallback |
| **SDK reliability** | In-memory batching, timed flush, never raises into the host |
| **Dashboard** | Dark UI: model, tokens, latency, cost; expand row for input/output |

---

## Quick start

### 1. Start the stack

```bash
git clone https://github.com/MhussainD4772/obsero.git
cd obsero
docker compose up -d
```

| Service | URL |
|---------|-----|
| API | http://localhost:8000/health |
| Events | http://localhost:8000/events |
| Postgres | `localhost:5433` (user/password/db: `obsero`) |

### 2. Run the dashboard (local recommended)

```bash
cd frontend
npm ci
npm run dev
```

Open http://localhost:3000  

> Prefer local `npm run dev` for the UI. Using Compose frontend and host Next against the same `frontend/` folder can conflict on the `.next` cache.

### 3. Send an event (SDK)

```bash
source backend/.venv/bin/activate   # or any venv
pip install -e ./sdk

python -c "import obsero; obsero.track('hello', {'ok': True})"
```

Refresh the dashboard.

### 4. Capture a real Gemini call (optional)

```bash
# .env at repo root: GEMINI_API_KEY=...
set -a && source .env && set +a
python sdk/examples/gemini_chat.py
```

---

## Architecture

```
Your app
  └─ obsero SDK (Python / httpx)
        │  track / trace → buffer → POST /events/batch
        ▼
FastAPI  ──►  PostgreSQL
        │
        └── GET /events
                ▼
         Next.js dashboard
```

| Layer | Stack |
|-------|--------|
| SDK | Python, httpx |
| Backend | FastAPI, async SQLAlchemy, Pydantic v2, Alembic |
| Database | PostgreSQL |
| Frontend | Next.js (App Router), TypeScript, Tailwind, TanStack Query |
| Infra | Docker Compose |

---

## Project layout

```
obsero/
├── backend/          # FastAPI + Alembic
├── frontend/         # Next.js dashboard
├── sdk/              # Installable Python package (obsero)
├── docs/             # Changelog, ADRs, devlog, future work
└── docker-compose.yml
```

---

## Documentation

| Doc | Purpose |
|-----|---------|
| [docs/CHANGELOG.md](docs/CHANGELOG.md) | What shipped |
| [docs/progress-sprint-01.md](docs/progress-sprint-01.md) | Sprint 01 wrap-up (OB-1 → OB-10) |
| [docs/adr/](docs/adr/) | Architecture decisions |
| [docs/devlog/](docs/devlog/) | Engineering journal |
| [docs/future-work.md](docs/future-work.md) | Deferred / post-v0 ideas |

---

## Development

```bash
# Backend checks (from CI)
cd backend && ruff check . && ruff format --check .

# Frontend checks (from CI)
cd frontend && npm ci && npm run lint && npm run format:check && npx tsc --noEmit
```

PRs against `main` require green CI. Direct pushes to `main` are blocked.

---

## Roadmap (toward v1.0)

- [x] Ingest + list events
- [x] LLM fields, cost estimate, batching, fail-safe SDK
- [x] Dashboard LLM columns + expand
- [ ] Nested-span tracing
- [ ] Cost / latency analytics
- [ ] Datasets + LLM-as-judge evals
- [ ] Auth & projects
- [ ] One-command self-host polish + tagged `v0.1` release

---

## Contributing

This is an early, ticket-driven project. Useful PRs:

1. Fix bugs or docs in the current vertical slice
2. Keep changes small and focused
3. Match existing stack conventions (no drive-by framework swaps)

Open an issue before large features.

---

## License

License not chosen yet. A `LICENSE` file will be added before the first tagged release.
