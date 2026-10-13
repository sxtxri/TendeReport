__all__ = ["ModelBase"]

import sqlalchemy

class ModelBase(sqlalchemy.orm.DeclarativeBase):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)