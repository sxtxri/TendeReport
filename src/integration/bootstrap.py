import functools

from common.telemetry import HttpMetricsClientType
from infrastructure.clients.base_http_client import MonitoredClientMixin
from infrastructure.db.repositories import PostgresTenderRepository
from integration.services.tender import TenderIntegrationService


@functools.cache
def get_tender_integration_service() -> TenderIntegrationService:
    return TenderIntegrationService(
        http_client=MonitoredClientMixin(client_type=HttpMetricsClientType.INTEGRATION),
        tender_repository=PostgresTenderRepository(),
    )
