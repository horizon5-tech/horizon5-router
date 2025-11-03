from typing import Any, Dict, List, Optional

from apps.core.interfaces.repository import RepositoryInterface
from apps.core.services.mongodb import MongoDBService


class BaseRepository(RepositoryInterface):
    # ───────────────────────────────────────────────────────────
    # PROPERTIES
    # ───────────────────────────────────────────────────────────
    _collection_name: str
    _db_service: MongoDBService

    # ───────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────
    def __init__(self, collection_name: str) -> None:
        self._collection_name = collection_name
        self._db_service = MongoDBService()

    # ───────────────────────────────────────────────────────────
    # PUBLIC METHODS
    # ───────────────────────────────────────────────────────────
    def find(
        self,
        limit: int = 10,
        offset: int = 0,
        sort_by: Optional[str] = None,
        sort_direction: str = "desc",
        query_filters: Optional[Dict[str, Any]] = None,
        projection_fields: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        collection = self._db_service.get_collection(self._collection_name)
        filters = query_filters or {}
        projection = projection_fields or {}
        cursor = collection.find(filters, projection)

        if sort_by and sort_direction:
            direction = -1 if sort_direction == "desc" else 1
            cursor = cursor.sort(sort_by, direction)

        if offset:
            cursor = cursor.skip(offset)

        if limit:
            cursor = cursor.limit(limit)

        return list(cursor)

    def count(
        self,
        query_filters: Optional[Dict[str, Any]] = None,
    ) -> int:
        collection = self._db_service.get_collection(self._collection_name)
        filters = query_filters or {}
        return collection.count_documents(filters)
