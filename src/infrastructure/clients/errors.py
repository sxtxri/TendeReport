from common.errors.base import BaseError


class ClientRequestError(BaseError):
    """Запрос не прошёл"""


class InvalidResponseError(BaseError):
    """Запрос прошёл успешно, тело ответа отличается от схемы"""
