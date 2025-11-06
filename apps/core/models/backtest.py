import logging
from typing import Any, Dict

from apps.core.enums.report_status import ReportStatus
from apps.core.models.base import BaseModel
from apps.core.repositories.backtest import BacktestRepository
from apps.core.repositories.order import OrderRepository
from apps.core.repositories.report import ReportRepository
from apps.core.repositories.snapshot import SnapshotRepository


class BacktestModel(BaseModel):
    # ───────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────
    def __init__(self) -> None:
        super().__init__()
        self._logger = logging.getLogger("django")
        self._repository = BacktestRepository()
        self._report_repository = ReportRepository()
        self._snapshot_repository = SnapshotRepository()
        self._order_repository = OrderRepository()

    def store(self, data: Dict[str, Any]) -> str:
        inserted_id = super().store(
            data=data,
        )

        if inserted_id:
            self._report_repository.store(
                data={
                    "backtest_id": inserted_id,
                    "status": ReportStatus.PENDING.value,
                    "folder": None,
                }
            )

        return inserted_id

    def delete(self, query_filters: Dict[str, Any]) -> bool:
        backtest_id_raw = query_filters.get("_id")
        backtest_id = str(backtest_id_raw) if backtest_id_raw else None
        response = super().delete(
            query_filters=query_filters,
        )

        if response and backtest_id:
            self._report_repository.delete_many(
                query_filters={
                    "backtest_id": backtest_id,
                }
            )

            self._snapshot_repository.delete_many(
                query_filters={
                    "backtest_id": backtest_id,
                }
            )

            self._order_repository.delete_many(
                query_filters={
                    "backtest_id": backtest_id,
                }
            )

        return True
