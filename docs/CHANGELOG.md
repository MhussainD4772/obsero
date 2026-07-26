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

### Changed

- Postgres host port mapped to `5433` to avoid clash with local Postgres on `5432`

### Fixed

- _what broke and got repaired_

<!--
## [0.1.0] - YYYY-MM-DD

### Added

- …
-->
