from typing import Generic, TypeVar

from pydantic.functional_validators import model_validator
from starlette.responses import JSONResponse

from api.base.exception_handlers.base import GeneralErrorInformationSchema
from common.schemas.camel import BaseCamelCaseSchema

DataT = TypeVar("DataT")


class RefinedJSONResponse(JSONResponse):
    media_type = "application/json; charset=utf-8"


class ObjectAPIResponse(BaseCamelCaseSchema, Generic[DataT]):
    """
    Схема ответа с единственным объектом.
    """

    data: DataT


class _Items(BaseCamelCaseSchema, Generic[DataT]):
    """
    Схема списка объектов.
    """

    items: list[DataT]


class ItemsAPIResponse(BaseCamelCaseSchema, Generic[DataT]):
    """
    Схема ответа со списком объектов.
    """

    data: _Items[DataT]
    items_per_page: int | None = None
    start_index: int | None = None
    current_item_count: int | None = None
    total_results: int | None = None

    @model_validator(mode="after")
    def calculate_items_count(self):
        if self.start_index is not None and self.items_per_page is not None:
            self.current_item_count = len(self.data.items)
        return self


class ErrorAPIResponse(BaseCamelCaseSchema):
    """
    Схема ответа с ошибкой.
    """

    error: GeneralErrorInformationSchema
