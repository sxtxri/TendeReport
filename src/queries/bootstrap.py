import functools

from infrastructure.db.repositories import PostgresTenderRepository
from queries.services import TenderService


@functools.cache
def get_tender_service() -> TenderService:
    return TenderService(tender_repository=PostgresTenderRepository())
