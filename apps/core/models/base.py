from typing import Any, Dict, List, Optional

from apps.core.repositories.base import BaseRepository


class BaseModel:
    # ───────────────────────────────────────────────────────────
    # PROPERTIES
    # ───────────────────────────────────────────────────────────
    _repository: BaseRepository

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
        return self._repository.find(
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            sort_direction=sort_direction,
            query_filters=query_filters,
            projection_fields=projection_fields,
        )

    def count(
        self,
        query_filters: Optional[Dict[str, Any]] = None,
    ) -> int:
        return self._repository.count(
            query_filters=query_filters,
        )

    def store(
        self,
        data: Dict[str, Any],
    ) -> str:
        return self._repository.store(
            data=data,
        )

    def store_many(
        self,
        data: List[Dict[str, Any]],
    ) -> List[str]:
        return self._repository.store_many(
            data=data,
        )

    def update(
        self,
        query_filters: Dict[str, Any],
        data: Dict[str, Any],
    ) -> int:
        return self._repository.update(
            query_filters=query_filters,
            data=data,
        )

    def delete(
        self,
        query_filters: Dict[str, Any],
    ) -> int:
        return self._repository.delete(
            query_filters=query_filters,
        )
