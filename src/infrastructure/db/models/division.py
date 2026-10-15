__all__ = ["DivisionModel"]


from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from common.types import DivisionName
from infrastructure.db.models.base import ModelBase


class DivisionModel(ModelBase):
    __tablename__ = "division"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    division_name: Mapped[DivisionName] = mapped_column(String(100), nullable=False)
