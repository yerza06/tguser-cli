"""SQLAlchemy async engine and session factory."""

from __future__ import annotations

from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from .models import Base

_engine: AsyncEngine | None = None
_sessionmaker: async_sessionmaker | None = None


def _make_url(db_path: Path) -> str:
    return f"sqlite+aiosqlite:///{db_path}"


async def init_db(db_path: Path) -> async_sessionmaker:
    """Lazily create the engine and tables, and return the session factory."""
    global _engine, _sessionmaker

    if _sessionmaker is None:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        _engine = create_async_engine(_make_url(db_path), future=True)
        _sessionmaker = async_sessionmaker(_engine, expire_on_commit=False)
        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    return _sessionmaker
