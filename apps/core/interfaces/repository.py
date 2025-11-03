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
