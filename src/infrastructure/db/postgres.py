from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import logging_settings, settings

alchemy_async_engine = create_async_engine(
    url=settings.POSTGRES_DSN,
    pool_size=settings.POSTGRES_POOL_MIN_SIZE,
    max_overflow=settings.POSTGRES_POOL_MAX_SIZE - settings.POSTGRES_POOL_MIN_SIZE,
    # В Linux tcp_keepalive_time по умолчанию 7200,
    # В postgres tcp_keepalives_idle по умолчанию 0,
    # выбираем значение меньше 7200.
    pool_recycle=600,
    pool_pre_ping=True,
    echo=logging_settings.IS_NEED_LOG_SQL_QUERIES,
)
async_session_factory = async_sessionmaker(alchemy_async_engine)