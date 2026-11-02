__all__ = ["NotificationClientType"]

import enum


class NotificationClientType(enum.StrEnum):
    FAKE = "fake"
    VK = "vk"
