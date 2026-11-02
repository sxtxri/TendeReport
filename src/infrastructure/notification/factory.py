__all__ = ["NotificationClientFactory"]

import functools

from config import settings
from infrastructure.logger.setup import get_logger
from infrastructure.notification.clients import (
    BaseNotificationClient,
    FakeNotificationClient,
    VkNotificationClient,
)
from infrastructure.notification.enums import NotificationClientType


class NotificationClientFactory:
    _logger = get_logger("NotificationClientFactory")

    @classmethod
    @functools.cache
    def build(cls) -> BaseNotificationClient:
        if settings.notification.CLIENT == NotificationClientType.VK:
            try:
                return VkNotificationClient(
                    token=settings.notification.VK_TOKEN,
                    peer_id=settings.notification.VK_PEER_ID,
                    api_version=settings.notification.VK_API_VERSION,
                )
            except Exception as exc:
                cls._logger.error(str(exc))

        return FakeNotificationClient()
