__all__ = ["ClientNotificationFactory"]

from typing import Any

from config import NotificationClientType, settings
from infrastructure.clients.base_http_client import MonitoredClientMixin
from infrastructure.clients.notification.base import BaseNotificationClient
from infrastructure.clients.notification.fake import FakeNotificationClient
from infrastructure.clients.notification.vk import VkNotificationClient


class ClientNotificationFactory:
    @classmethod
    def create(
        cls,
        client_type: str | NotificationClientType | None = None,
        token: str | None = None,
        peer_id: int | str | None = None,
        api_version: str | None = None,
        http_client: MonitoredClientMixin | None = None,
        **kwargs: Any,
    ) -> BaseNotificationClient:
        resolved_type = client_type or settings.NOTIFICATION_CLIENT
        if isinstance(resolved_type, str):
            resolved_type = resolved_type.lower()

        if resolved_type == NotificationClientType.VK:
            vk_token = token or settings.VK_TOKEN or settings.notification.VK_TOKEN
            vk_peer_id = peer_id or settings.VK_PEER_ID or settings.notification.VK_PEER_ID
            vk_api_version = (
                api_version
                or settings.VK_API_VERSION
                or settings.notification.VK_API_VERSION
            )
            return VkNotificationClient(
                token=vk_token,
                peer_id=vk_peer_id,
                api_version=vk_api_version,
                http_client=http_client,
                **kwargs,
            )

        if resolved_type == NotificationClientType.FAKE:
            return FakeNotificationClient(**kwargs)

        raise ValueError(
            f"Неподдерживаемый тип клиента уведомлений: '{resolved_type}'. "
            f"Допустимые значения: {[t.value for t in NotificationClientType]}"
        )

    @classmethod
    def build(cls, *args, **kwargs) -> BaseNotificationClient:
        """Алиас к create."""
        return cls.create(*args, **kwargs)

    @classmethod
    def create_client(cls, *args, **kwargs) -> BaseNotificationClient:
        """Алиас к create."""
        return cls.create(*args, **kwargs)
