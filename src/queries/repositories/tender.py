__all__ = ["BaseTenderRepository"]

from common.types import TenderId
from queries.entities import Tender
from queries.repositories.base import BaseRepository


class BaseTenderRepository(BaseRepository):
    async def get_tender(self, tender_id: TenderId) -> Tender:
        raise NotImplementedError
