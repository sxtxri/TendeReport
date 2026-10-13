__all__ = ["TenderService"]

from queries.repositories import TenderRepository
from queries.entities import Tender
from common.types import TenderId


class TenderService:
    def __init__(self, tender_repository: TenderRepository):
        self._tender_repository = tender_repository

    async def get_tender(self, tender_id: TenderId) -> Tender:
        pass
