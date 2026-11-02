import functools

from common.telemetry import HttpMetricsClientType
from config import settings
from infrastructure.clients.base_http_client import MonitoredClientMixin
from infrastructure.db.repositories import PostgresTenderRepository
from infrastructure.notification.clients import BaseNotificationClient
from infrastructure.notification.factory import NotificationClientFactory
from infrastructure.notification.service import NotificationService
from infrastructure.scrappers import BaseScrapper, GazpromNeftZakupkiScrapper
from integration.services.tender import TenderIntegrationService


@functools.cache
def get_scrapper_async_client() -> MonitoredClientMixin:
    return MonitoredClientMixin(
        client_type=HttpMetricsClientType.INTEGRATION, headers={"User-Agent": settings.scrapper.USER_AGENT}
    )


@functools.cache
def get_gazprom_neft_zakupki() -> BaseScrapper:
    return GazpromNeftZakupkiScrapper(client=get_scrapper_async_client())


@functools.cache
def get_notification_client() -> BaseNotificationClient:
    return NotificationClientFactory.build()


@functools.cache
def get_notification_service() -> NotificationService:
    return NotificationService(client=get_notification_client())


@functools.cache
def get_tender_integration_service() -> TenderIntegrationService:
    return TenderIntegrationService(
        tender_repository=PostgresTenderRepository(),
        scrappers=[
            get_gazprom_neft_zakupki(),
        ],
        notification_service=get_notification_service(),
    )
