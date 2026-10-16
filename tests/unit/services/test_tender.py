from datetime import date, datetime
from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from common.errors.errors import BaseNotFoundError
from queries.entities import Tender
from queries.services import TenderService


def make_tender(**overrides) -> Tender:
    defaults = dict(
        id=1,
        title="Разработка сервиса",
        company="ООО Карьера в карьере",
        city="Москва",
        description=None,
        estimated_price=Decimal("1000.00"),
        division_id=None,
        division_name=None,
        published_at=None,
        application_deadline=None,
        contract_deadline=None,
        summary_deadline=None,
        platform_url=None,
        scoring=None,
        created_at=datetime(2026, 1, 1),
        updated_at=datetime(2026, 1, 1),
    )
    defaults.update(overrides)
    return Tender(**defaults)


@pytest.fixture
def tender_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def tender_service(tender_repo: AsyncMock) -> TenderService:
    return TenderService(tender_repo)


class TestTenderService:
    async def test_get_tender(self, tender_service: TenderService, tender_repo: AsyncMock):
        tender = make_tender(id=42)
        tender_repo.get_tender.return_value = tender

        result = await tender_service.get_tender(tender_id=42)

        assert result == tender
        tender_repo.get_tender.assert_awaited_once_with(tender_id=42)

    async def test_get_tender_not_found(self, tender_service: TenderService, tender_repo: AsyncMock):
        tender_repo.get_tender.return_value = None

        with pytest.raises(BaseNotFoundError):
            await tender_service.get_tender(tender_id=404)

    async def test_find_tenders(self, tender_service: TenderService, tender_repo: AsyncMock):
        tenders = [make_tender(id=1), make_tender(id=2)]
        tender_repo.find_tenders.return_value = tenders
        tender_repo.count_tenders.return_value = len(tenders)

        deadline_from = date(2026, 1, 1)
        deadline_to = date(2026, 12, 31)

        result_tenders, result_count = await tender_service.find_tenders(
            city="Москва",
            application_deadline_from=deadline_from,
            application_deadline_to=deadline_to,
            is_price_defined=True,
            limit=10,
            offset=5,
        )

        assert result_tenders == tenders
        assert result_count == len(tenders)
        tender_repo.find_tenders.assert_awaited_once_with(
            city="Москва",
            application_deadline_from=deadline_from,
            application_deadline_to=deadline_to,
            is_price_defined=True,
            limit=10,
            offset=5,
        )
        tender_repo.count_tenders.assert_awaited_once_with(
            city="Москва",
            application_deadline_from=deadline_from,
            application_deadline_to=deadline_to,
            is_price_defined=True,
        )

    async def test_find_tenders_defaults(self, tender_service: TenderService, tender_repo: AsyncMock):
        tender_repo.find_tenders.return_value = []
        tender_repo.count_tenders.return_value = 0

        result_tenders, result_count = await tender_service.find_tenders()

        assert result_tenders == []
        assert result_count == 0
        tender_repo.find_tenders.assert_awaited_once_with(
            city=None,
            application_deadline_from=None,
            application_deadline_to=None,
            is_price_defined=None,
            limit=20,
            offset=0,
        )

    async def test_get_cities(self, tender_service: TenderService, tender_repo: AsyncMock):
        tender_repo.get_cities.return_value = ["Москва", "Санкт-Петербург"]

        result = await tender_service.get_cities()

        assert result == ["Москва", "Санкт-Петербург"]
        tender_repo.get_cities.assert_awaited_once_with()
