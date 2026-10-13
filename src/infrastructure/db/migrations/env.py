import asyncio
from logging.config import fileConfig
from os import environ

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine

config = context.config

section = config.config_ini_section
config.set_section_option(
    section,
    "POSTGRES_DB_USER",
    environ.get("POSTGRES_DB_USER"),
)
config.set_section_option(
    section,
    "POSTGRES_DB_PASSWORD",
    environ.get("POSTGRES_DB_PASSWORD"),
)
config.set_section_option(
    section,
    "POSTGRES_DB_NAME",
    environ.get("POSTGRES_DB_NAME"),
)
config.set_section_option(
    section,
    "POSTGRES_DB_HOST",
    environ.get("POSTGRES_DB_HOST"),
)
config.set_section_option(
    section,
    "POSTGRES_DB_PORT",
    environ.get("POSTGRES_DB_PORT"),
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# TODO: пока непонятно надо ли импортировать именнно здесь
from infrastructure.db.models.base import ModelBase  # noqa: E402

target_metadata = ModelBase.metadata


def include_object(obj, name, type_, reflected, compare_to):
    """
    Exclude views from Alembic's consideration.
    """
    return not obj.info.get("is_view", False)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
