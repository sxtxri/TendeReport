__all__ = ["TenderModel"]

from datetime import datetime
from sqlalchemy import String, Text, Integer, DateTime, func, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.db.models.base import ModelBase


class TenderModel(ModelBase):
    __tablename__ = "tender"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String(100)), nullable=True)
    scoring: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # дата публикации тендера
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # время создания записи
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), server_default=func.now(), nullable=False
    )

    # время обновления записи
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
    )