__all__ = ["NotificationService"]

from infrastructure.logger.setup import get_logger
from infrastructure.notification.clients import BaseNotificationClient
from infrastructure.notification.errors import NotificationError

logger = get_logger("NotificationService")


class NotificationService:
    def __init__(self, client: BaseNotificationClient) -> None:
        self.client = client

    async def send_notification(self, message: str) -> None:
        try:
            await self.client.send_message(message)
        except NotificationError as exc:
            logger.info(str(exc))
        except Exception as exc:
            logger.error(str(exc))
