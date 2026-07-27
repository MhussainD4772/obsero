#!/bin/sh
set -e
# Image may predate alembic in requirements; install if missing.
python -c "import alembic" 2>/dev/null || pip install -q "alembic==1.14.0"
alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
