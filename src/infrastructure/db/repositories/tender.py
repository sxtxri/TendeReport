__all__ = ["PostgresTenderRepository"]

from datetime import date

from sqlalchemy import delete, func, select, update
from sqlalchemy.orm import selectinload

from common.types import TenderId
from infrastructure.db.factories import TenderFactory
from infrastructure.db.models import TenderModel
from infrastructure.db.session import get_db_session
from queries.entities import Tender
from queries.repositories import BaseTenderRepository


class PostgresTenderRepository(BaseTenderRepository):
    async def get_tender(self, tender_id: TenderId) -> Tender | None:
        async with get_db_session() as session:
            sql = select(TenderModel).where(TenderModel.id == tender_id).options(selectinload(TenderModel.division))
            result = (await session.scalars(sql)).one_or_none()

            return TenderFactory.orm_to_domain(result) if result else None

    async def find_tenders(
        self,
        city: str | None = None,
        application_deadline_from: date | None = None,
        application_deadline_to: date | None = None,
        is_price_defined: bool | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Tender]:
        async with get_db_session() as session:
            sql = (
                self._apply_filters(
                    select(TenderModel).options(selectinload(TenderModel.division)),
                    city=city,
                    application_deadline_from=application_deadline_from,
                    application_deadline_to=application_deadline_to,
                    is_price_defined=is_price_defined,
                )
                .order_by(TenderModel.id)
                .limit(limit)
                .offset(offset)
            )

            result = (await session.scalars(sql)).all()

            return [TenderFactory.orm_to_domain(tender) for tender in result]

    async def count_tenders(
        self,
        city: str | None = None,
        application_deadline_from: date | None = None,
        application_deadline_to: date | None = None,
        is_price_defined: bool | None = None,
    ) -> int:
        async with get_db_session() as session:
            sql = self._apply_filters(
                select(func.count(TenderModel.id)),
                city=city,
                application_deadline_from=application_deadline_from,
                application_deadline_to=application_deadline_to,
                is_price_defined=is_price_defined,
            )

            return (await session.scalars(sql)).one()

    async def get_cities(self) -> list[str]:
        async with get_db_session() as session:
            sql = select(TenderModel.city).distinct().where(TenderModel.city.is_not(None))
            result = (await session.scalars(sql)).all()

            return list(result)

    async def mark_all_need_deleted(self) -> None:
        async with get_db_session() as session:
            sql = update(TenderModel).values({TenderModel.need_deleted: True})
            await session.execute(sql)

            await session.commit()

    async def delete_all_need_deleted(self) -> None:
        async with get_db_session() as session:
            sql = delete(TenderModel).where(TenderModel.need_deleted.is_(True))
            await session.execute(sql)

            await session.commit()

    @staticmethod
    def _apply_filters(
        sql: select,
        city: str | None,
        application_deadline_from: date | None,
        application_deadline_to: date | None,
        is_price_defined: bool | None,
    ) -> select:
        if city is not None:
            sql = sql.where(TenderModel.city == city)
        if application_deadline_from is not None:
            sql = sql.where(TenderModel.application_deadline >= application_deadline_from)
        if application_deadline_to is not None:
            sql = sql.where(TenderModel.application_deadline <= application_deadline_to)
        if is_price_defined is not None:
            sql = sql.where(
                TenderModel.estimated_price.is_not(None) if is_price_defined else TenderModel.estimated_price.is_(None)
            )
        return sql
