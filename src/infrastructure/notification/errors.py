__all__ = ["NotificationError", "VkNotificationError"]

from common.errors.base import BaseError


class NotificationError(BaseError):
    """Ошибка при отправке уведомления"""


class VkNotificationError(NotificationError):
    """Ошибка при отправке уведомления через VK API"""
