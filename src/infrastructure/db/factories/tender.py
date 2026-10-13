__all__ = ["TenderFactory"]

from infrastructure.db.factories.base import BaseFactory
from infrastructure.db.models import TenderModel
from queries.entities import Tender


class TenderFactory(BaseFactory):
    @classmethod
    def orm_to_domain(cls, orm_model: TenderModel) -> Tender:
        return Tender(
            id=orm_model.id,
            name=orm_model.name,
            company=orm_model.company,
            description=orm_model.description,
            tag=orm_model.tag,
            scoring=orm_model.scoring,
            published_at=orm_model.published_at,
        )

    @classmethod
    def domain_to_orm(cls, domain_model: Tender) -> TenderModel:
        return TenderModel(
            id=domain_model.id,
            name=domain_model.name,
            company=domain_model.company,
            description=domain_model.description,
            tags=domain_model.tags,
            scoring=domain_model.scoring,
            published_at=domain_model.published_at,
        )
