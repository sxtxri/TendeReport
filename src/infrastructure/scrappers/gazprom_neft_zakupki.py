__all__ = ["GazpromNeftZakupkiScrapper"]


from urllib.parse import urljoin

from bs4 import BeautifulSoup

from infrastructure.scrappers.base import BaseScrapper
from infrastructure.scrappers.endpoints import ScrapperEndpoint

# карточка тендера на странице листинга
_TENDER_CARD_CLASS = "purchase-container"
# ссылка на детальную страницу тендера внутри карточки
_TENDER_LINK_CLASS = "purchase-number"


class GazpromNeftZakupkiScrapper(BaseScrapper):
    ENDPOINT = ScrapperEndpoint.GAZPROM_NEFT_ZAKUPKI

    async def scrape_page(self) -> list[str]:
        pages: list[str] = []
        page_number = 1

        while True:
            response = await self.client.get(self.ENDPOINT, params={"PAGE": page_number})
            response.raise_for_status()

            html = response.text
            if _TENDER_CARD_CLASS not in html:
                break

            pages.append(html)
            page_number += 1

        return pages

    async def scrape_item(self) -> list[str]:
        tender_urls = [url for page_html in await self.scrape_page() for url in self._extract_tender_urls(page_html)]

        tenders_html = []
        for tender_url in tender_urls:
            response = await self.client.get(tender_url)
            response.raise_for_status()
            tenders_html.append(response.text)

        return tenders_html

    def _extract_tender_urls(self, page_html: str) -> list[str]:
        soup = BeautifulSoup(page_html, "lxml")

        urls = []
        for card in soup.find_all(class_=_TENDER_CARD_CLASS):
            link = card.find(class_=_TENDER_LINK_CLASS)
            anchor = link.find("a", href=True) if link else None
            if anchor:
                urls.append(urljoin(f"{self.ENDPOINT}/", anchor["href"]))

        return urls
