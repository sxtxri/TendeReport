__all__ = ["TenderIntegrationService"]

from infrastructure.clients.base_http_client import MonitoredClientMixin
from infrastructure.scrappers import BaseScrapper
from queries.repositories import BaseTenderRepository


class TenderIntegrationService:
    def __init__(
        self,
        http_client: MonitoredClientMixin,
        tender_repository: BaseTenderRepository,
        scrappers: list[BaseScrapper],
    ):
        self._http_client = http_client
        self._tender_repository = tender_repository
        self._scrappers = scrappers

    async def integrate(self) -> None:
        raise NotImplementedError
