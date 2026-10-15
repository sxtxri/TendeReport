__all__ = ["TenderService"]

from datetime import date

from common.errors.errors import BaseNotFoundError
from common.types import TenderId
from queries.entities import Tender
from queries.repositories import BaseTenderRepository
from utils.async_tools import run_concurrent


class TenderService:
    def __init__(self, tender_repository: BaseTenderRepository):
        self._tender_repository = tender_repository

    async def get_tender(self, tender_id: TenderId) -> Tender | None:
        tender: Tender | None = await self._tender_repository.get_tender(tender_id=tender_id)
        if tender is not None:
            return tender
        raise BaseNotFoundError(f"Тендер с id={tender_id} не найден")

    async def find_tenders(
        self,
        city: str | None = None,
        application_deadline_from: date | None = None,
        application_deadline_to: date | None = None,
        is_price_defined: bool | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Tender], int]:
        find_tenders_task = self._tender_repository.find_tenders(
            city=city,
            application_deadline_from=application_deadline_from,
            application_deadline_to=application_deadline_to,
            is_price_defined=is_price_defined,
            limit=limit,
            offset=offset,
        )
        count_tenders_task = self._tender_repository.count_tenders(
            city=city,
            application_deadline_from=application_deadline_from,
            application_deadline_to=application_deadline_to,
            is_price_defined=is_price_defined,
        )

        tenders, tenders_count = await run_concurrent(find_tenders_task, count_tenders_task)

        return tenders, tenders_count

    async def get_cities(self) -> list[str]:
        return await self._tender_repository.get_cities()
