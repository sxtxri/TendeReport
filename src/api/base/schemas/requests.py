from typing import Generic, TypeVar

from pydantic import BaseModel

DataT = TypeVar("DataT")


class BaseAPIRequest(BaseModel, Generic[DataT]):
    data: DataT