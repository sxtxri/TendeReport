__all__ = ["TenderIntegrationService"]

from infrastructure.notification.service import NotificationService
from infrastructure.scrappers import BaseScrapper
from queries.repositories import BaseTenderRepository
from utils.async_tools import run_concurrent


class TenderIntegrationService:
    def __init__(
        self,
        tender_repository: BaseTenderRepository,
        scrappers: list[BaseScrapper],
        notification_service: NotificationService,
    ):
        self._tender_repository = tender_repository
        self._scrappers = scrappers
        self._notification_service = notification_service

    async def integrate(self) -> None:
        await self._tender_repository.mark_all_need_deleted()
        await self._integrate()
        await self._tender_repository.delete_all_need_deleted()
        await self._notification_service.send_notification(
            "Интеграция данных по тендерам успешно завершена"
        )

    async def _integrate(self) -> None:
        tasks = []
        for scrapper in self._scrappers:
            tasks.append(scrapper.scrape())
        await run_concurrent(*tasks)
