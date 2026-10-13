__all__ = ["TenderService"]

from common.errors.errors import BaseNotFoundError
from common.types import TenderId
from queries.entities import Tender
from queries.repositories import BaseTenderRepository


class TenderService:
    def __init__(self, tender_repository: BaseTenderRepository):
        self._tender_repository = tender_repository

    async def get_tender(self, tender_id: TenderId) -> Tender | None:
        tender: Tender | None = await self._tender_repository.get_tender(tender_id=tender_id)
        if tender is not None:
            return tender
        raise BaseNotFoundError(f"Тендер с id={tender_id} не найден")
