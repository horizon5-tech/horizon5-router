from datetime import UTC, datetime
from typing import Any, Dict, List, Optional

from apps.core.enums.report_status import ReportStatus
from apps.core.repositories.base import BaseRepository
from apps.core.repositories.report import ReportRepository


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
        return self._repository.count(query_filters=query_filters)

    def store(
        self,
        data: Dict[str, Any],
    ) -> str:
        inserted_id = self._repository.store(data=data)

        if inserted_id:
            ReportRepository().store(
                data={
                    "backtest_id": inserted_id,
                    "status": ReportStatus.PENDING.value,
                    "created_at": datetime.now(tz=UTC),
                    "updated_at": datetime.now(tz=UTC),
                }
            )

        return inserted_id

    def update(
        self,
        query_filters: Dict[str, Any],
        data: Dict[str, Any],
    ) -> int:
        data["updated_at"] = datetime.now(tz=UTC)
        return self._repository.update(
            query_filters=query_filters,
            data=data,
        )

    def delete(
        self,
        query_filters: Dict[str, Any],
    ) -> int:
        return self._repository.delete(query_filters=query_filters)
