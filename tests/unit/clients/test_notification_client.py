from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from common.telemetry import HttpMetricsClientType
from config import NotificationClientType
from infrastructure.clients.base_http_client import MonitoredClientMixin
from infrastructure.clients.errors import VkNotificationError
from infrastructure.clients.notification.base import BaseNotificationClient
from infrastructure.clients.notification.factory import ClientNotificationFactory
from infrastructure.clients.notification.fake import FakeNotificationClient
from infrastructure.clients.notification.vk import VkNotificationClient


class TestFakeNotificationClient:
    async def test_fake_notification_client_logs_message(self):
        mock_logger = MagicMock()
        client = FakeNotificationClient(log=mock_logger)

        assert isinstance(client, BaseNotificationClient)
        assert not isinstance(client, MonitoredClientMixin)

        await client.send_message("Test message")

        mock_logger.info.assert_called_once_with(
            "Fake notification sent",
            message="Test message",
        )


class TestVkNotificationClient:
    def test_vk_client_inheritance(self):
        client = VkNotificationClient(token="test_token", peer_id="123456")

        assert isinstance(client, BaseNotificationClient)
        assert isinstance(client, MonitoredClientMixin)
        assert isinstance(client, httpx.AsyncClient)
        assert client._client_type == HttpMetricsClientType.NOTIFICATION

    async def test_vk_client_send_message_success(self):
        mock_http_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": 999}
        mock_response.raise_for_status.return_value = None
        mock_http_client.post.return_value = mock_response

        client = VkNotificationClient(
            token="test_token",
            peer_id=123456,
            api_version="5.199",
            http_client=mock_http_client,
        )

        result = await client.send_message("Привет из интеграции!")

        assert result == {"response": 999}
        mock_http_client.post.assert_awaited_once()

        call_args = mock_http_client.post.await_args
        assert call_args.args[0] == "https://api.vk.com/method/messages.send"

        data = call_args.kwargs["data"]
        assert data["access_token"] == "test_token"
        assert data["peer_id"] == "123456"
        assert data["message"] == "Привет из интеграции!"
        assert data["v"] == "5.199"
        assert "random_id" in data
        assert isinstance(data["random_id"], int)

    async def test_vk_client_send_message_api_error(self):
        mock_http_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "error": {
                "error_code": 100,
                "error_msg": "One of the parameters specified was missing or invalid: peer_id is undefined",
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_http_client.post.return_value = mock_response

        client = VkNotificationClient(
            token="test_token",
            peer_id="123456",
            http_client=mock_http_client,
        )

        with pytest.raises(VkNotificationError) as exc_info:
            await client.send_message("Привет!")

        assert "100" in str(exc_info.value)
        assert "peer_id is undefined" in str(exc_info.value)


class TestClientNotificationFactory:
    def test_create_fake_client(self):
        client = ClientNotificationFactory.create(client_type=NotificationClientType.FAKE)
        assert isinstance(client, FakeNotificationClient)

    def test_create_fake_client_from_string(self):
        client = ClientNotificationFactory.create(client_type="fake")
        assert isinstance(client, FakeNotificationClient)

    def test_create_vk_client(self):
        client = ClientNotificationFactory.create(
            client_type=NotificationClientType.VK,
            token="vk_token_123",
            peer_id="999",
        )
        assert isinstance(client, VkNotificationClient)
        assert client._token == "vk_token_123"
        assert client._peer_id == "999"

    def test_create_unknown_client_raises_value_error(self):
        with pytest.raises(ValueError) as exc_info:
            ClientNotificationFactory.create(client_type="telegram")
        assert "Неподдерживаемый тип клиента" in str(exc_info.value)
