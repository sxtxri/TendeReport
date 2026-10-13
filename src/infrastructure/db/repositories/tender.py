__all__ = ["PostgresTenderRepository"]

from sqlalchemy import select

from common.types import TenderId
from infrastructure.db.factories import TenderFactory
from infrastructure.db.models import TenderModel
from infrastructure.db.session import get_db_session
from queries.entities import Tender
from queries.repositories import BaseTenderRepository


class PostgresTenderRepository(BaseTenderRepository):
    async def get_tender(self, tender_id: TenderId) -> Tender | None:
        async with get_db_session() as session:
            sql = select(TenderModel).where(TenderModel.id == tender_id)
            result = (await session.scalars(sql)).one_or_none()

            return TenderFactory.orm_to_domain(result) if result else None
