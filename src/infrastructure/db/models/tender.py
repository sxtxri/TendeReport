__all__ = ["TenderModel"]

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    false,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db.models.base import ModelBase
from infrastructure.db.models.division import DivisionModel


class TenderModel(ModelBase):
    __tablename__ = "tender"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Название тендера",
    )
    company: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Компания-заказчик",
    )
    city: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Город",
    )
    division_id: Mapped[int | None] = mapped_column(
        ForeignKey("division.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Направление тендера",
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Описание тендера",
    )
    estimated_price: Mapped[float | None] = mapped_column(
        Numeric(18, 2),
        nullable=True,
        comment="Ориентировочная цена",
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="Дата публикации тендера",
    )

    application_deadline: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="Срок подачи заявки",
    )
    contract_deadline: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="Срок исполнения договора",
    )
    summary_deadline: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="Срок подведения итогов",
    )

    platform_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="URL площадки",
    )

    scoring: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Скоринг (оценка релевантности) тендера",
    )

    need_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=false(),
        nullable=False,
        comment="Тендер помечен к удалению как отсутствующий на площадке",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        server_default=func.now(),
        nullable=False,
        comment="Дата и время создания записи",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
        comment="Дата и время последнего обновления записи",
    )

    division: Mapped[DivisionModel | None] = relationship("DivisionModel")
