__all__ = ["Tender"]

from datetime import datetime

from common.types import TenderId
from queries.entities.base import Entity


class Tender(Entity):
    id: TenderId

    name: str
    company: str
    description: str | None
    tag: list[str] | None
    scoring: int | None

    published_at: datetime | None

    @property
    def entity_id(self) -> TenderId:
        return self.id
