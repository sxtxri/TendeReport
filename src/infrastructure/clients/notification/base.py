__all__ = ["BaseNotificationClient"]

import abc


class BaseNotificationClient(abc.ABC):
    """Базовый абстрактный клиент для отправки уведомлений."""

    @abc.abstractmethod
    async def send_message(self, message: str) -> None:
        """Отправить сообщение получателю."""
        raise NotImplementedError

    async def send_notification(self, message: str) -> None:
        """Отправить уведомление."""
        await self.send_message(message)
