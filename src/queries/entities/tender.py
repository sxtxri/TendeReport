__all__ = ["Tender"]

from datetime import datetime
from decimal import Decimal

from common.types import DivisionId, DivisionName, TenderId
from queries.entities.base import Entity


class Tender(Entity):
    id: TenderId

    title: str
    company: str
    city: str | None
    description: str | None
    estimated_price: Decimal | None
    division_id: DivisionId | None
    division_name: DivisionName | None

    published_at: datetime | None
    application_deadline: datetime | None
    contract_deadline: datetime | None
    summary_deadline: datetime | None

    platform_url: str | None
    scoring: int | None

    created_at: datetime
    updated_at: datetime

    @property
    def entity_id(self) -> TenderId:
        return self.id
