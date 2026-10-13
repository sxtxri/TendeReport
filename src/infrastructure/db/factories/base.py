__all__ = ["BaseFactory"]

import abc

from pydantic import BaseModel

from queries.entities import Entity


class BaseFactory(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def orm_to_domain(cls, orm_model: BaseModel) -> Entity:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def domain_to_orm(cls, domain_model: Entity) -> BaseModel:
        raise NotImplementedError
