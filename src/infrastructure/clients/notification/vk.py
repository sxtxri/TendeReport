__all__ = ["VkNotificationClient"]

import random
from typing import Any

import structlog
from httpx import Response

from common.telemetry import HttpMetricsClientType
from infrastructure.clients.base_http_client import MonitoredClientMixin
from infrastructure.clients.errors import VkNotificationError
from infrastructure.clients.notification.base import BaseNotificationClient

logger = structlog.get_logger(__name__)


class VkNotificationClient(BaseNotificationClient, MonitoredClientMixin):

    VK_API_URL = "https://api.vk.com/method/messages.send"

    def __init__(
        self,
        token: str,
        peer_id: int | str,
        api_version: str = "5.199",
        client_type: Any = HttpMetricsClientType.NOTIFICATION,
        http_client: MonitoredClientMixin | None = None,
        *args,
        **kwargs,
    ):
        self._token = token
        self._peer_id = str(peer_id)
        self._api_version = api_version
        self._external_client = http_client
        super().__init__(client_type=client_type, *args, **kwargs)

    async def send_message(self, message: str) -> dict[str, Any]:
        random_id = random.randint(1, 2**31 - 1)
        payload = {
            "access_token": self._token,
            "peer_id": self._peer_id,
            "message": message,
            "random_id": random_id,
            "v": self._api_version,
        }

        response = await self._send_request(payload)
        response.raise_for_status()

        data: dict[str, Any] = response.json()

        if "error" in data:
            error_data = data["error"]
            error_code = error_data.get("error_code")
            error_msg = error_data.get("error_msg", "Unknown VK API error")
            logger.error(
                "VK API returned error response",
                error_code=error_code,
                error_msg=error_msg,
                peer_id=self._peer_id,
            )
            raise VkNotificationError(f"VK API error [{error_code}]: {error_msg}")

        logger.info(
            "VK message sent successfully",
            peer_id=self._peer_id,
            message_id=data.get("response"),
        )
        return data

    async def _send_request(self, payload: dict[str, Any]) -> Response:
        if self._external_client is not None:
            return await self._external_client.post(self.VK_API_URL, data=payload)
        return await self.post(self.VK_API_URL, data=payload)
