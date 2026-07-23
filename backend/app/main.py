from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.db import engine
from app.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: touch DB (fails loudly if down) + create tables
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))  # connectivity check
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: dispose connection pool
    await engine.dispose()


app = FastAPI(title="Obsero API", lifespan=lifespan)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
