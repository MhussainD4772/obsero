import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Inside Compose: host is service name "postgres". +asyncpg = async driver.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://obsero:obsero@postgres:5432/obsero",
)

# Engine = pool of async connections to Postgres
engine = create_async_engine(DATABASE_URL, echo=True)

# Session factory — each request gets its own AsyncSession
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # objects stay usable after commit
)


async def get_db():
    """FastAPI dependency: yield a session, always close it afterward."""
    async with AsyncSessionLocal() as session:
        yield session
