import os
from typing import Generator

import alembic.config
import pytest
import pytest_alembic
import yarl
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists, drop_database

from config import logging_settings, settings
from infrastructure.logger.setup import get_logger, setup_logging

AlembicConfig = alembic.config.Config
AlembicPytestConfig = pytest_alembic.config.Config


# TODO: пока инициализируем так, с фикстурами надо разобраться
setup_logging(app_settings=settings, logging_settings=logging_settings)


logger = get_logger(__name__)


# подключение для синхронного создания и удаления БД
@pytest.fixture(scope="session", autouse=True)
def postgres_dsn() -> str:
    dsn = yarl.URL(settings.POSTGRES_TEST_DSN)
    dsn = str(dsn.with_scheme("postgresql"))

    return dsn


# базу создаём только синхронно,
#   т.к. алхимия по-другому относительно просто делать не умеет
@pytest.fixture(scope="session")
def setup_db(postgres_dsn: str) -> Generator[None, None, None]:
    logger.info("SETUP database")

    if not settings.APPLY_MIGRATIONS_FOR_TESTS:
        logger.info("applying migrations disabled..")
        yield
        return

    if database_exists(postgres_dsn):
        drop_database(postgres_dsn)

    create_database(postgres_dsn)

    yield

    drop_database(postgres_dsn)

    logger.info("TEARDOWN database")


@pytest.fixture(scope="session")
def alembic_db_session(setup_db, postgres_dsn: str) -> Generator[Session, Session, None]:
    logger.info("SETUP session")

    if not settings.APPLY_MIGRATIONS_FOR_TESTS:
        logger.info("applying migrations disabled..")
        yield
        return

    engine = create_engine(
        url=postgres_dsn,
        pool_size=settings.POSTGRES_POOL_MIN_SIZE,
        max_overflow=settings.POSTGRES_POOL_MAX_SIZE - settings.POSTGRES_POOL_MIN_SIZE,
        # В Linux tcp_keepalive_time по умолчанию 7200,
        # В postgres tcp_keepalives_idle по умолчанию 0,
        # выбираем значение меньше 7200.
        pool_recycle=600,
        pool_pre_ping=True,
        echo=logging_settings.IS_NEED_LOG_SQL_QUERIES,
    )

    session = None
    try:
        session = Session(engine)
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

    logger.info("TEARDOWN session")


@pytest.fixture(scope="session")
def alembic_engine(alembic_db_session: AsyncSession) -> Generator[Session, Session, None]:
    logger.info("SETUP alembic engine")

    if not settings.APPLY_MIGRATIONS_FOR_TESTS:
        logger.info("applying migrations disabled..")
        yield
        return

    yield alembic_db_session.get_bind()

    logger.info("TEARDOWN alembic engine")


@pytest.fixture(scope="session")
def alembic_config(alembic_db_session: AsyncSession) -> AlembicConfig | None:
    logger.info("SETUP alembic config")

    if not settings.APPLY_MIGRATIONS_FOR_TESTS:
        logger.info("applying migrations disabled..")
        return None

    # FIXME: убрать костыль фикса относительных путей при запуске тестов из дебага
    ini_file_path = str(settings.BASE_DIR / "alembic.ini")
    path_to_migrations = str(settings.BASE_DIR / "infrastructure" / "db" / "migrations")

    cfg = alembic.config.Config(ini_file_path)
    cfg.set_main_option("script_location", path_to_migrations)

    return cfg


@pytest.fixture(scope="session")
def alembic_runner(alembic_config: AlembicConfig, alembic_engine):
    logger.info("SETUP alembic runner")

    if not settings.APPLY_MIGRATIONS_FOR_TESTS:
        logger.info("applying migrations disabled..")
        yield
        return

    config = AlembicPytestConfig.from_raw_config(alembic_config)
    with pytest_alembic.runner(config=config, engine=alembic_engine) as runner:
        yield runner

    logger.info("TEARDOWN alembic runner")


@pytest.fixture(scope="session")
def apply_migrations(alembic_runner):
    logger.info("SETUP alembic migration")

    if not settings.APPLY_MIGRATIONS_FOR_TESTS:
        logger.info("applying migrations disabled..")
        yield
        return

    # пишем контекст для алембика
    os.environ["POSTGRES_DB_USER"] = settings.POSTGRES_DB_USER
    os.environ["POSTGRES_DB_PASSWORD"] = settings.POSTGRES_DB_PASSWORD
    os.environ["POSTGRES_DB_NAME"] = settings.POSTGRES_TEST_DB_NAME
    os.environ["POSTGRES_DB_HOST"] = settings.POSTGRES_DB_HOST
    os.environ["POSTGRES_DB_PORT"] = str(settings.POSTGRES_DB_PORT)

    alembic_runner.migrate_up_to("head")

    yield

    # миграции не откатываем, т.к. удаляем БД
    logger.info("TEARDOWN alembic migration")
