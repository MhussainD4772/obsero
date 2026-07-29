# Obsero — Sprint 01 progress (OB-1 → OB-10)

**Dates:** 2026-07-21 → 2026-07-28  
**Board:** all tickets **Done** · Repo: https://github.com/MhussainD4772/obsero  
**Merged:** PRs #1–#11 (incl. clean dark UI)

**What you have now:** end-to-end LLM observability slice — wrap a call → cost + tokens + latency in Postgres → see it on a dark dashboard (expand for I/O).

```
App code
  → obsero.trace / track()
  → buffer → POST /events/batch
  → Postgres (LLM columns)
        ↑
Browser ← GET /events ←────────┘
(localhost:3000)     (localhost:8000)
```

---

## Ticket by ticket

| Ticket | What | Outcome |
|--------|------|---------|
| **OB-1** | Monorepo + Compose | `backend/`, `frontend/`, `sdk/`; `docker compose up` → Postgres, FastAPI `/health`, Next.js; CI (lint/format/types/ruff) |
| **OB-2** | DB + `events` table | Async SQLAlchemy + asyncpg; `Event` model; host Postgres on **5433** |
| **OB-3** | Events HTTP API | `POST /events` + `GET /events` (newest first); Pydantic create/read |
| **OB-4** | Python SDK | `pip install -e ./sdk`; `obsero.track()` via httpx; `init` / `OBSERO_BASE_URL` |
| **OB-5** | Events list UI + CORS | TanStack Query table; CORS for `:3000`; Refresh + `cache: "no-store"` |
| **OB-6** | Alembic owns schema | `migrations/` + `0001_create_events`; drop `create_all`; entrypoint `upgrade head` |
| **OB-7** | Real LLM fields | Nullable provider/model/I/O/tokens/latency/cost/status; migration `0002` |
| **OB-8** | Capture a real LLM call | ADR 0002 (context manager); `obsero.trace`; Gemini example (`gemini-flash-latest`) |
| **OB-9** | Cost, batch, fail-safe | Pricing table; buffer + size/time flush; `POST /events/batch`; never raise into host |
| **OB-10** | Dashboard LLM UI | Model, tokens, latency, cost columns; expand row for input/output; nulls → — |

**Also shipped (not a numbered ticket):** clean dark UI + `motion`; `docs/future-work.md`; Prettier path fix; Compose anonymous `/app/.next` volume.

---

## How to run it today

```bash
docker compose up -d   # postgres + backend (UI often local — see below)
# API:  http://localhost:8000/health  and  /events
# DB:   127.0.0.1:5433  (user/pass/db: obsero)
```

```bash
cd frontend && npm run dev   # preferred for UI (avoid Docker+host Next fighting over .next)
# UI: http://localhost:3000
```

```bash
source backend/.venv/bin/activate
pip install -e ./sdk
set -a && source .env && set +a   # GEMINI_API_KEY for the example
python sdk/examples/gemini_chat.py
# Refresh the dashboard — expand a row for input/output
```

Fail-safe check (optional): `docker compose stop backend` → `track` + `flush` → host still prints OK (warning only).

---

## Stack (locked)

| Layer | Choice |
|-------|--------|
| Frontend | Next.js App Router, TypeScript, Tailwind, TanStack Query, `motion` |
| Backend | FastAPI, async SQLAlchemy, Pydantic v2, Alembic |
| Data | PostgreSQL |
| SDK | Python + httpx (+ `google-genai` for Gemini example) |
| Infra | Docker Compose |
| UI | Clean dark (zinc-950) — `.cursor/rules/clean-dark-ui.mdc` (local) |

---

## Key files

| Area | Paths |
|------|--------|
| Compose | `docker-compose.yml` |
| API | `backend/app/main.py`, `db.py`, `models.py`, `schemas.py` |
| Migrations | `backend/migrations/versions/0001_*.py`, `0002_*.py` |
| SDK | `sdk/src/obsero/{client,trace,pricing}.py`, `sdk/examples/gemini_chat.py` |
| UI | `frontend/app/page.tsx`, `components/events-table.tsx`, `lib/api.ts` |
| Decisions | `docs/adr/0002-sdk-instrumentation-shape.md` |
| Deferred | `docs/future-work.md` |
| Notes | `docs/devlog/sprint-01.md`, `docs/CHANGELOG.md` |

---

## Learning highlights (factual)

- Compose service DNS (`postgres`) vs host tools (`localhost:5433`)
- Alembic vs `create_all`; don’t name the package folder `alembic/`
- CORS is a browser concern; SDK/curl don’t need it
- Browser caches `GET` JSON — `cache: "no-store"` for Refresh
- Observability SDK must not take down the host (fail-safe flush)
- `Decimal` isn’t JSON-safe — send cost as string
- Docker Next cache under `/app` poisons local `npm run dev` — isolate `.next`

---

## Not done yet (next sprint / post-v0)

See `docs/future-work.md` and the product pillars still ahead:

- Nested spans / real traces, cost/latency analytics charts  
- Datasets & LLM-as-judge evals, auth & projects  
- Pricing overrides / backend-owned rates, durable buffers  
- Real OSS README + cut **`v0.1.0`** from `[Unreleased]` (still pending)  
- Optional: new `docs/devlog/sprint-02.md` when the next sprint starts  

---

Same story in shorter form: `docs/CHANGELOG.md` (one-liners) and `docs/devlog/sprint-01.md` (per-ticket “What I built”; Why / fought / learned still yours to fill).
