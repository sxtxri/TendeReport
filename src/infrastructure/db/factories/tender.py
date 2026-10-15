__all__ = ["TenderFactory"]

from infrastructure.db.factories.base import BaseFactory
from infrastructure.db.models import TenderModel
from queries.entities import Tender


class TenderFactory(BaseFactory):
    @classmethod
    def orm_to_domain(cls, orm_model: TenderModel) -> Tender:
        return Tender(
            id=orm_model.id,
            title=orm_model.title,
            company=orm_model.company,
            city=orm_model.city,
            description=orm_model.description,
            estimated_price=orm_model.estimated_price,
            division_id=orm_model.division_id,
            division_name=orm_model.division.division_name if orm_model.division else None,
            published_at=orm_model.published_at,
            application_deadline=orm_model.application_deadline,
            contract_deadline=orm_model.contract_deadline,
            summary_deadline=orm_model.summary_deadline,
            platform_url=orm_model.platform_url,
            scoring=orm_model.scoring,
            created_at=orm_model.created_at,
            updated_at=orm_model.updated_at,
        )

    @classmethod
    def domain_to_orm(cls, domain_model: Tender) -> TenderModel:
        return TenderModel(
            id=domain_model.id,
            title=domain_model.title,
            company=domain_model.company,
            city=domain_model.city,
            description=domain_model.description,
            estimated_price=domain_model.estimated_price,
            division_id=domain_model.division_id,
            published_at=domain_model.published_at,
            application_deadline=domain_model.application_deadline,
            contract_deadline=domain_model.contract_deadline,
            summary_deadline=domain_model.summary_deadline,
            platform_url=domain_model.platform_url,
            scoring=domain_model.scoring,
            created_at=domain_model.created_at,
            updated_at=domain_model.updated_at,
        )
