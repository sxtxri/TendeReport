__all__ = ["SearchQueryFactory"]

from infrastructure.db.factories.base import BaseFactory
from infrastructure.db.models import SearchQueryModel
from queries.entities import SearchQuery


class SearchQueryFactory(BaseFactory):
    @classmethod
    def orm_to_domain(cls, orm_model: SearchQueryModel) -> SearchQuery:
        return SearchQuery(
            id=orm_model.id,
            division_id=orm_model.division_id,
            division_name=orm_model.division.division_name,
            search_queries=orm_model.search_queries,
        )

    @classmethod
    def domain_to_orm(cls, domain_model: SearchQuery) -> SearchQueryModel:
        return SearchQueryModel(
            id=domain_model.id,
            division_id=domain_model.division_id,
            search_queries=domain_model.search_queries,
        )
