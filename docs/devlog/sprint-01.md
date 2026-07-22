# Sprint 01

**Dates:** 2026-07-21 → _end_  
**Goal:** Stand up the monorepo + Docker Compose spine (OB-1)

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

## Ticket: _next ticket key_

### What I built

_Same headings as above — copy this block per ticket._

### Why (key decisions)

_

### What fought me

_

### What I learned

_
