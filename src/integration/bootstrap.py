import functools

from common.telemetry import HttpMetricsClientType
from config import settings
from infrastructure.clients.base_http_client import MonitoredClientMixin
from infrastructure.clients.notification.base import BaseNotificationClient
from infrastructure.clients.notification.factory import ClientNotificationFactory
from infrastructure.db.repositories import PostgresTenderRepository
from infrastructure.scrappers import BaseScrapper, GazpromNeftZakupkiScrapper
from integration.services.notification import NotificationService
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
    return ClientNotificationFactory.create()


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
