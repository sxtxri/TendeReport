__all__ = ["BaseScrapper"]

from infrastructure.clients.base_http_client import MonitoredClientMixin


class BaseScrapper:
    def __init__(self, client: MonitoredClientMixin):
        self.client = client

    async def scrape_page(self) -> str:
        raise NotImplementedError

    async def scrape_item(self) -> str:
        raise NotImplementedError
