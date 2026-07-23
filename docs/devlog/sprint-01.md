# Sprint 01

**Dates:** 2026-07-21 → _end_  
**Goal:** Stand up monorepo + Compose (OB-1), then wire Postgres + events table (OB-2)

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

## Ticket: _next ticket key_

### What I built

_Same headings as above — copy this block per ticket._

### Why (key decisions)

_

### What fought me

_

### What I learned

_
