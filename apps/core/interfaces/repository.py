from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class RepositoryInterface(ABC):
    # ───────────────────────────────────────────────────────────
    # PUBLIC METHODS
    # ───────────────────────────────────────────────────────────
    @abstractmethod
    def find(
        self,
        limit: int = 10,
        offset: int = 0,
        sort_by: Optional[str] = None,
        sort_direction: str = "desc",
        query_filters: Optional[Dict[str, Any]] = None,
        projection_fields: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def count(
        self,
        query_filters: Optional[Dict[str, Any]] = None,
    ) -> int:
        pass

    @abstractmethod
    def store(
        self,
        data: Dict[str, Any],
    ) -> str:
        pass

    @abstractmethod
    def store_many(
        self,
        data: List[Dict[str, Any]],
    ) -> List[str]:
        pass

    @abstractmethod
    def update(
        self,
        query_filters: Dict[str, Any],
        data: Dict[str, Any],
    ) -> int:
        pass

    @abstractmethod
    def delete(
        self,
        query_filters: Dict[str, Any],
    ) -> int:
        pass

    @abstractmethod
    def delete_many(
        self,
        query_filters: Dict[str, Any],
    ) -> int:
        pass
