__all__ = ["SearchQueryModel"]


from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.types import DivisionId
from infrastructure.db.models.base import ModelBase
from infrastructure.db.models.division import DivisionModel


class SearchQueryModel(ModelBase):
    __tablename__ = "search_query"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    division_id: Mapped[DivisionId] = mapped_column(
        ForeignKey("division.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    search_queries: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)

    division: Mapped[DivisionModel] = relationship("DivisionModel")
