import logging
import logging.config
import os
import sys

import structlog
from structlog.typing import FilteringBoundLogger

from config import LoggingSettings, Settings


def _add_app_context(service_name: str):
    def processor(logger, method_name, event_dict):
        event_dict.setdefault("service", service_name)
        return event_dict

    return processor


def _shared_processors() -> list:
    return [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]


def _plain_processors() -> list:
    return _shared_processors() + [
        structlog.dev.ConsoleRenderer(colors=sys.stdout.isatty()),
    ]


def _json_processors() -> list:
    return _shared_processors() + [
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(),
    ]


def _build_logging_config(
    default_log_level: str,
    uvicorn_log_level: str,
    uvicorn_access_log_level: str,
    is_enabled_debug_mode: bool,
    http_log_level: str,
    use_json: bool,
) -> dict:
    root_level = "DEBUG" if is_enabled_debug_mode else default_log_level

    formatter_name = "json" if use_json else "plain"

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "plain": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(colors=sys.stdout.isatty()),
                "foreign_pre_chain": _shared_processors(),
            },
            "json": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(),
                "foreign_pre_chain": _shared_processors(),
            },
        },
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "formatter": formatter_name,
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {  # root
                "handlers": ["default"],
                "level": root_level,
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["default"],
                "level": uvicorn_log_level,
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["default"],
                "level": uvicorn_log_level,
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["default"],
                "level": uvicorn_access_log_level,
                "propagate": False,
            },
            # убираем шум от asgi_correlation_id
            "asgi_correlation_id": {
                "handlers": ["default"],
                "level": "ERROR",
                "propagate": False,
            },
            # убираем шум от httpx/httpcore
            "httpx": {
                "handlers": ["default"],
                "level": http_log_level,
                "propagate": False,
            },
            "httpcore": {
                "handlers": ["default"],
                "level": http_log_level,
                "propagate": False,
            },
        },
    }


def setup_logging(app_settings: Settings, logging_settings: LoggingSettings) -> None:
    use_json = not (app_settings.is_local or app_settings.is_test_env)

    structlog.configure(
        processors=_shared_processors()
        + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    if use_json:
        structlog.configure(
            processors=_json_processors() + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
    else:
        structlog.configure(
            processors=_plain_processors() + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

    logging_config = _build_logging_config(
        default_log_level=logging_settings.DEFAULT_LOG_LEVEL,
        uvicorn_log_level=logging_settings.UVICORN_LOG_LEVEL,
        uvicorn_access_log_level=logging_settings.UVICORN_ACCESS_LOG_LEVEL,
        is_enabled_debug_mode=app_settings.DEBUG,
        http_log_level=getattr(logging_settings, "HTTPX_LOG_LEVEL", "WARNING"),
        use_json=use_json,
    )

    logging.config.dictConfig(logging_config)


def get_logger(logger_name: str = "") -> FilteringBoundLogger:
    if not logger_name:
        logger_name = os.getenv("SERVICE_NAME", "app")
    return structlog.get_logger(logger_name)
