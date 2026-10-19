__all__ = ["FakeNotificationClient"]

import structlog
from structlog.typing import FilteringBoundLogger

from infrastructure.clients.notification.base import BaseNotificationClient

logger = structlog.get_logger(__name__)


class FakeNotificationClient(BaseNotificationClient):
    def __init__(self, log: FilteringBoundLogger | None = None):
        self._logger = log or logger

    async def send_message(self, message: str) -> None:
        self._logger.info("Fake notification sent", message=message)
