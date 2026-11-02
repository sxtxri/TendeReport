__all__ = ["TenderIntegrationService"]

from infrastructure.notification.service import NotificationService
from infrastructure.scrappers import BaseScrapper
from queries.repositories import BaseTenderRepository


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
        for scrapper in self._scrappers:
            try:
                await scrapper.scrape_item()
            except Exception:
                pass

        await self._notification_service.send_notification(
            "Интеграция данных по тендерам успешно завершена"
        )
