from pydantic import BaseModel


class BaseError(Exception):
    """
    Базовая ошибка.
    """

    msg: str = ""

    def __init__(self, msg=None):
        if msg:
            self.msg = msg

    def __str__(self) -> str:
        return f"Msg: {self.msg}"


class ErrorSchema(BaseModel):
    """
    Модель ошибки.
    """

    message: str
    reason: str
