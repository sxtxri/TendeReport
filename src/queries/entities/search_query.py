__all__ = ["SearchQuery"]

from common.types import DivisionId, DivisionName, SearchQueryId
from queries.entities.base import Entity


class SearchQuery(Entity):
    id: SearchQueryId
    division_id: DivisionId
    division_name: DivisionName
    search_queries: list[str]

    @property
    def entity_id(self) -> SearchQueryId:
        return self.id
