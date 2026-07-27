# Database migrations (Alembic)

Schema is owned by Alembic, not `create_all`.

## Commands

From `backend/` (host, DB on published port 5433):

```bash
export DATABASE_URL='postgresql+asyncpg://obsero:obsero@localhost:5433/obsero'
alembic upgrade head      # apply
alembic current          # show version
alembic revision --autogenerate -m "msg"  # after model changes
```

Inside Compose (service DNS `postgres`):

```bash
docker compose exec backend alembic upgrade head
```

## Existing DB that already has tables

If `events` was created by the old `create_all` path, stamp once instead of creating again:

```bash
alembic stamp head
```

## Fresh DB DoD

`alembic upgrade head` alone must create `events` + `alembic_version`.
