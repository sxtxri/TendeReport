import asyncio
import contextlib
from contextlib import asynccontextmanager
from typing import Iterator

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.postgres import async_session_factory

__all__ = ["db_session", "get_db_session"]


@asynccontextmanager
async def db_session() -> Iterator[AsyncSession]:
    session = async_session_factory()
    try:
        yield session
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        with contextlib.suppress(asyncio.TimeoutError):
            # implementation of shielded cancel with timeout
            async with asyncio.timeout(5):  # noqa: ASYNC102
                await session.close()  # noqa: ASYNC102


@asynccontextmanager
async def get_db_session() -> Iterator[AsyncSession]:
    async with db_session() as session:
        yield session
