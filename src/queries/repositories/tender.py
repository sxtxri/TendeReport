__all__ = ["BaseTenderRepository"]

from queries.repositories.base import BaseRepository
from common.types import TenderId
from queries.entities import Tender


class BaseTenderRepository(BaseRepository):
    async def get_tender(self, tender_id: TenderId) -> Tender:
        raise NotImplementedError