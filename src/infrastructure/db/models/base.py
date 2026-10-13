__all__ = ["ModelBase"]

from sqlalchemy import Column, Integer
from sqlalchemy.orm import DeclarativeBase


class ModelBase(DeclarativeBase):
    id = Column(Integer, primary_key=True)
