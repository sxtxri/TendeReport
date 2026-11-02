__all__ = ["FakeNotificationClient"]

import structlog

from infrastructure.notification.clients.base import BaseNotificationClient

logger = structlog.get_logger(__name__)


class FakeNotificationClient(BaseNotificationClient):
    async def send_message(self, message: str) -> None:
        logger.info("Fake notification sent", message=message)
