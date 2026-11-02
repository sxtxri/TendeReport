__all__ = ["BaseNotificationClient"]

from abc import ABC, abstractmethod


class BaseNotificationClient(ABC):
    """Базовый абстрактный клиент для отправки уведомлений."""

    @abstractmethod
    async def send_message(self, message: str) -> None:
        """Отправить сообщение получателю."""
        raise NotImplementedError
