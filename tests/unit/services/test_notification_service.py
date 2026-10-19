from unittest.mock import AsyncMock

from infrastructure.clients.notification.base import BaseNotificationClient
from integration.services.notification import NotificationService
from integration.services.tender import TenderIntegrationService


class TestNotificationService:
    async def test_send_notification_delegates_to_client(self):
        mock_client = AsyncMock(spec=BaseNotificationClient)
        service = NotificationService(client=mock_client)

        await service.send_notification("Интеграция завершена")

        mock_client.send_message.assert_awaited_once_with("Интеграция завершена")

    async def test_send_message_alias(self):
        mock_client = AsyncMock(spec=BaseNotificationClient)
        service = NotificationService(client=mock_client)

        await service.send_message("Тестовое сообщение")

        mock_client.send_message.assert_awaited_once_with("Тестовое сообщение")


class TestTenderIntegrationServiceNotification:
    async def test_integration_triggers_notification(self):
        mock_repo = AsyncMock()
        mock_scrapper = AsyncMock()
        mock_scrapper.scrape_item.return_value = ["tender_html_1", "tender_html_2"]
        mock_notification_service = AsyncMock(spec=NotificationService)

        service = TenderIntegrationService(
            tender_repository=mock_repo,
            scrappers=[mock_scrapper],
            notification_service=mock_notification_service,
        )

        await service.integrate()

        mock_scrapper.scrape_item.assert_awaited_once()
        mock_notification_service.send_notification.assert_awaited_once()
        sent_message = mock_notification_service.send_notification.await_args.args[0]
        assert "Интеграция данных по тендерам успешно завершена" in sent_message
