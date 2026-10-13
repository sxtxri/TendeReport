all = ["Entity", "ValueObject"]

from abc import ABC, abstractmethod

from common.schemas import BaseCamelCaseSchema


class Entity(BaseCamelCaseSchema, ABC):
    @property
    @abstractmethod
    def entity_id(self) -> str | int:
        raise NotImplementedError


class ValueObject(BaseCamelCaseSchema):
    class Config:
        frozen = True

    def eq(self, other: "ValueObject") -> bool:
        return self.model_dump() == other.model_dump()