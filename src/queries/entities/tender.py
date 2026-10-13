__all__ = ["Tender"]

from queries.entities.base import Entity
from common.types import TenderId
from datetime import datetime

class Tender(Entity):
    tender_id: TenderId

    name: str
    company: str
    description: str | None
    tag: list[str] | None
    scoring: int | None

    published_at: datetime | None