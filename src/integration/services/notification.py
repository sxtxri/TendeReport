__all__ = ["NotificationService"]

from infrastructure.clients.notification.base import BaseNotificationClient


class NotificationService:
    def __init__(self, client: BaseNotificationClient):
        self._client = client

    @property
    def client(self) -> BaseNotificationClient:
        return self._client

    async def send_notification(self, message: str) -> None:
        await self._client.send_message(message)

    async def send_message(self, message: str) -> None:
        await self._client.send_message(message)
