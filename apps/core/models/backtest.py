import logging
from typing import Any, Dict

from apps.core.enums.report_status import ReportStatus
from apps.core.models.base import BaseModel
from apps.core.repositories.backtest import BacktestRepository
from apps.core.repositories.report import ReportRepository


class BacktestModel(BaseModel):
    # ───────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────
    def __init__(self) -> None:
        super().__init__()
        self._logger = logging.getLogger("django")
        self._repository = BacktestRepository()
        self._report_repository = ReportRepository()

    def store(self, data: Dict[str, Any]) -> str:
        inserted_id = super().store(
            data=data,
        )

        if inserted_id:
            self._report_repository.store(
                data={
                    "backtest_id": inserted_id,
                    "status": ReportStatus.PENDING.value,
                }
            )

        return inserted_id

    def delete(self, query_filters: Dict[str, Any]) -> bool:
        response = super().delete(
            query_filters=query_filters,
        )

        if response:
            self._logger.info(
                f"Deleting report for backtest ID: {query_filters['_id']}"
            )

            self._report_repository.delete(
                query_filters={
                    "backtest_id": query_filters["_id"],
                }
            )

        return response > 0
