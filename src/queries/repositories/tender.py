__all__ = ["BaseTenderRepository"]

from datetime import date

from common.types import TenderId
from queries.entities import Tender
from queries.repositories.base import BaseRepository


class BaseTenderRepository(BaseRepository):
    async def get_tender(self, tender_id: TenderId) -> Tender:
        raise NotImplementedError

    async def find_tenders(
        self,
        city: str | None = None,
        application_deadline_from: date | None = None,
        application_deadline_to: date | None = None,
        is_price_defined: bool | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Tender]:
        raise NotImplementedError

    async def count_tenders(
        self,
        city: str | None = None,
        application_deadline_from: date | None = None,
        application_deadline_to: date | None = None,
        is_price_defined: bool | None = None,
    ) -> int:
        raise NotImplementedError

    async def get_cities(self) -> list[str]:
        raise NotImplementedError

    async def mark_all_need_deleted(self) -> None:
        raise NotImplementedError

    async def delete_all_need_deleted(self) -> None:
        raise NotImplementedError
