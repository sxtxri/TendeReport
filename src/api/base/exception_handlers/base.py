from typing import TypeVar

from pydantic import BaseModel, Field

from common.errors.base import ErrorSchema

ErrorSchemaType = TypeVar("ErrorSchemaType", bound=ErrorSchema)


class GeneralErrorInformationSchema(BaseModel):
    """
    Модель общей информации об ошибке.
    """

    message: str
    errors: list[ErrorSchemaType]
    service: str | None = Field(default=None)