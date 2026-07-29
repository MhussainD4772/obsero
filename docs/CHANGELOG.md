# Changelog

Format based on [Keep a Changelog](https://keepachangelog.com/).  
Versions follow [SemVer](https://semver.org/) as you cut releases (`v0.1` → `v1.0`).

**Habit:** one line per meaningful change under `[Unreleased]`.  
When you release, rename that block to the version + date and start a fresh `[Unreleased]`.

## [Unreleased]

### Added

- Monorepo Docker Compose scaffold: Postgres, FastAPI `/health`, Next.js (OB-1)
- GitHub Actions CI: frontend lint/format/types + backend ruff
- Async SQLAlchemy + `events` table; app creates schema on startup (OB-2)
- `POST /events` and `GET /events` (newest first) (OB-3)
- Installable Python SDK: `obsero.track()` → `POST /events`; configurable base URL (OB-4)
- Next.js events list (TanStack Query) + FastAPI CORS for `localhost:3000` (OB-5)
- Alembic migrations for schema; initial `events` revision (OB-6)
- Nullable LLM fields on `events` + migration `0002`; POST/GET /events accept and return them (OB-7)
- SDK `obsero.trace` context manager + Gemini example; `track()` sends LLM fields (OB-8)
- ADR 0002: context manager for LLM instrumentation; Gemini first for free-tier learning (OB-8)

### Changed

- Postgres host port mapped to `5433` to avoid clash with local Postgres on `5432`
- App startup no longer calls `create_all`; schema applied via `alembic upgrade head` (OB-6)
- Dashboard UI design system: clean dark mode (zinc-950) + `motion` for entrances

### Fixed

- Events list Refresh ignored updates when the browser cached `GET /events` (OB-5)

<!--
## [0.1.0] - YYYY-MM-DD

### Added

- …
-->
