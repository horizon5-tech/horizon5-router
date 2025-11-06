import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from bson import ObjectId
from django.conf import settings

from apps.core.enums.report_status import ReportStatus
from apps.core.models.backtest import BacktestModel
from apps.core.models.order import OrderModel
from apps.core.models.report import ReportModel
from apps.core.models.snapshot import SnapshotModel

logger = logging.getLogger("django")


class BacktestReportTask:
    # ───────────────────────────────────────────────────────────
    # PROPERTIES
    # ───────────────────────────────────────────────────────────
    _name: str = "make_backtest_report"
    _backtest_id: Optional[str]
    _backtest: Optional[Dict[str, Any]]
    _report: Optional[Dict[str, Any]]
    _orders: List[Dict[str, Any]]
    _snapshots: List[Dict[str, Any]]

    _ready: bool
    _folder: Optional[Path]

    # ───────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────
    def __init__(self, backtest_id: Optional[str] = None) -> None:
        self._backtest_id = backtest_id
        self._report_model = ReportModel()
        self._order_model = OrderModel()
        self._snapshot_model = SnapshotModel()
        self._ready = False
        self._setup()

    # ───────────────────────────────────────────────────────────
    # PUBLIC METHODS
    # ───────────────────────────────────────────────────────────
    def run(self) -> None:
        if (
            not self._report
            or not self._orders
            or not self._snapshots
            or not self._folder
        ):
            logger.error("Task is not ready")
            return

        orders = self._orders
        snapshots = self._snapshots
        report = self._report
        folder = self._folder

        report_id = report["_id"]

        self._update_report(
            report_id=report_id,
            data={"folder": str(folder)},
        )

    # ───────────────────────────────────────────────────────────
    # PRIVATE METHODS
    # ───────────────────────────────────────────────────────────
    def _setup(self) -> None:
        self._backtest = self._get_backtest_by_id(
            self._backtest_id,  # type: ignore
        )

        if not self._backtest_id or not self._backtest:
            logger.error("Failed to find backtest")
            return

        self._report = self._get_report_by_backtest_id(
            self._backtest["_id"],
        )

        if not self._report:
            logger.error("Failed to find report")
            return

        self._orders = self._get_orders_by_backtest_id(self._backtest["_id"])

        if len(self._orders) == 0:
            logger.error("Failed to find orders")
            return

        self._snapshots = self._get_snapshots_by_backtest_id(self._backtest["_id"])

        if len(self._snapshots) == 0:
            logger.error("Failed to find snapshots")
            return

        report_id = self._report["_id"]

        self._folder = Path(settings.BASE_DIR) / "storage" / "reports" / str(report_id)
        self._folder.mkdir(parents=True, exist_ok=True)
        self._ready = True

    def _get_backtest_by_id(self, backtest_id: str) -> Optional[Dict[str, Any]]:
        results = BacktestModel().find(
            query_filters={"_id": ObjectId(backtest_id)},
        )

        return results[0] if results else None

    def _get_report_by_backtest_id(self, backtest_id: str) -> Optional[Dict[str, Any]]:
        report = self._report_model.find(
            query_filters={"backtest_id": backtest_id},
        )

        return report[0] if report else None

    def _get_orders_by_backtest_id(self, backtest_id: str) -> List[Dict[str, Any]]:
        return self._order_model.find(
            limit=9**100,
            query_filters={
                "backtest": True,
                "backtest_id": backtest_id,
            },
            sort_by="created_at",
            sort_direction="asc",
        )

    def _get_snapshots_by_backtest_id(self, backtest_id: str) -> List[Dict[str, Any]]:
        return self._snapshot_model.find(
            limit=9**100,
            query_filters={"backtest_id": backtest_id},
            sort_by="created_at",
            sort_direction="asc",
        )

    def _update_report(self, report_id: str, data: Dict[str, Any]) -> None:
        self._report_model.update(
            query_filters={"_id": ObjectId(report_id)},
            data=data,
        )

    def _update_report_to_failed(self, report_id: str) -> None:
        self._update_report(
            report_id=report_id,
            data={
                "status": ReportStatus.FAILED.value,
            },
        )
