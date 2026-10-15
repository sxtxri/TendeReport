__all__ = ["TenderIntegrationService"]

from infrastructure.scrappers import BaseScrapper
from queries.repositories import BaseTenderRepository


class TenderIntegrationService:
    def __init__(
        self,
        tender_repository: BaseTenderRepository,
        scrappers: list[BaseScrapper],
    ):
        self._tender_repository = tender_repository
        self._scrappers = scrappers

    async def integrate(self) -> None:
        raise NotImplementedError
