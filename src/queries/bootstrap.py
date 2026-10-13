import functools

from queries.repositories import TenderRepository
from queries.services import TenderService


@functools.cache
def get_tender_service() -> TenderService:
    return TenderService(
        tender_repository=TenderRepository()
    )