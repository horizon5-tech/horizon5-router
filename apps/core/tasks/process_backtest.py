import logging
from datetime import UTC, datetime
from typing import Any, Dict, List, Optional

from celery import shared_task

from apps.core.enums.backtest_status import BacktestStatus
from apps.core.enums.report_status import ReportStatus
from apps.core.repositories.backtest import BacktestRepository
from apps.core.repositories.order import OrderRepository
from apps.core.repositories.report import ReportRepository

logger = logging.getLogger("django")


class ProcessBacktestTask:
    # ───────────────────────────────────────────────────────────
    # PROPERTIES
    # ───────────────────────────────────────────────────────────
    _name: str = "process_backtest"

    # ───────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────
    def __init__(self) -> None:
        self._backtest_repository = BacktestRepository()
        self._report_repository = ReportRepository()
        self._order_repository = OrderRepository()

    # ───────────────────────────────────────────────────────────
    # PUBLIC METHODS
    # ───────────────────────────────────────────────────────────
    def run(self) -> None:
        logger.info(f"Processing task: {self._name}")

        pending_backtests = self._get_pending_backtests()

        logger.info(f"Found {len(pending_backtests)} pending backtests")

        for backtest in pending_backtests:
            backtest_id = str(backtest["_id"])
            session_id = backtest["session_id"]
            report_id = None
            report = self._get_report_by_backtest_id(backtest_id)

            if report:
                report_id = report["_id"]
                logger.info(f"Report: {report_id}")

            else:
                report_id = self._create_report(
                    {
                        "backtest_id": backtest_id,
                        "status": ReportStatus.BUILDING.value,
                    }
                )

                logger.info(f"Report: {report_id}")

            orders = self._get_orders_by_backtest_id(session_id)
            logger.info(f"Found {len(orders)} orders for backtest {backtest_id}")

    # ───────────────────────────────────────────────────────────
    # PRIVATE METHODS
    # ───────────────────────────────────────────────────────────
    def _get_pending_backtests(self) -> List[Dict[str, Any]]:
        return self._backtest_repository.find(
            query_filters={
                "status": BacktestStatus.COMPLETED.value,
                "$or": [
                    {"report_id": None},
                    {"report_id": {"$exists": False}},
                ],
            },
        )

    def _get_report_by_backtest_id(self, backtest_id: str) -> Optional[Dict[str, Any]]:
        report = self._report_repository.find(
            query_filters={"backtest_id": backtest_id},
        )

        return report[0] if report else None

    def _get_orders_by_backtest_id(self, session_id: str) -> List[Dict[str, Any]]:
        return self._order_repository.find(
            limit=9**100,
            query_filters={
                "backtest": True,
                "backtest_id": session_id,
            },
        )

    def _create_report(self, data: Dict[str, Any]) -> str:
        return self._report_repository.store(
            data=data,
        )


@shared_task(name="apps.core.tasks.process_backtest")
def process_backtest() -> Dict[str, Any]:
    task = ProcessBacktestTask()
    task.run()

    return {
        "status": "success",
        "time": datetime.now(tz=UTC),
    }
