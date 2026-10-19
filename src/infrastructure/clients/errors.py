from common.errors.base import BaseError
from common.telemetry import HttpMetricsClientType


class ClientRequestError(BaseError):
    """Запрос не прошёл"""


class UnSuccessfulRequestError(BaseError):
    """Запрос прошёл, код ответа не тот"""

    def __init__(self, msg: str, status_code: int, service: HttpMetricsClientType | None = None):
        super().__init__(msg)
        self.status_code = status_code
        self.service = service

    def __str__(self) -> str:
        return f"Service: {self.service} | Status code: {self.status_code} | Msg: {self.msg}"


class InvalidResponseError(BaseError):
    """Запрос прошёл успешно, тело ответа отличается от схемы"""


class NotificationError(BaseError):
    """Ошибка при отправке уведомления"""


class VkNotificationError(NotificationError):
    """Ошибка при отправке уведомления через VK API"""
