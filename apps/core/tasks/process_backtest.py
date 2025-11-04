import logging
from datetime import UTC, datetime
from typing import Any, Dict, List, Optional, Tuple

from bson import ObjectId
from celery import shared_task

from apps.core.enums.report_status import ReportStatus
from apps.core.helpers.get_cagr_from import get_cagr_from
from apps.core.helpers.get_calmar_ratio_from import get_calmar_ratio_from
from apps.core.helpers.get_cvar_from import get_cvar_from
from apps.core.helpers.get_max_drawdown_from import get_max_drawdown_from
from apps.core.helpers.get_profit_factor_from import get_profit_factor_from
from apps.core.helpers.get_r2_from import get_r2_from
from apps.core.helpers.get_recovery_factor_from import get_recovery_factor_from
from apps.core.helpers.get_sharpe_ratio_from import get_sharpe_ratio_from_orders
from apps.core.helpers.get_sortino_ratio_from import get_sortino_ratio_from
from apps.core.helpers.get_ulcer_index_from import get_ulcer_index_from
from apps.core.models.backtest import BacktestModel
from apps.core.models.order import OrderModel
from apps.core.models.report import ReportModel
from apps.core.models.report_performances import ReportPerformancesModel
from apps.core.models.report_returns import ReportReturnsModel
from apps.core.models.snapshot import SnapshotModel

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
        self._report_model = ReportModel()
        self._report_returns_model = ReportReturnsModel()
        self._report_performances_model = ReportPerformancesModel()
        self._order_model = OrderModel()
        self._snapshot_model = SnapshotModel()

    # ───────────────────────────────────────────────────────────
    # PUBLIC METHODS
    # ───────────────────────────────────────────────────────────
    def run(self, backtest_id: Optional[str] = None) -> None:
        backtest = self._get_backtest_by_id(
            backtest_id,  # type: ignore
        )

        if not backtest_id or not backtest:
            logger.error(f"Failed to find backtest by id: {backtest_id}")
            return

        report = self._get_report_by_backtest_id(backtest_id)
        orders = self._get_orders_by_backtest_id(backtest_id)
        snapshots = self._get_snapshots_by_backtest_id(backtest_id)

        if not report:
            logger.error(f"Failed to find report by backtest id: {backtest_id}")
            return

        if len(snapshots) == 0:
            logger.error(f"Failed to find snapshots by backtest id: {backtest_id}")
            self._cancel_report(report_id=report["_id"])
            return

        if len(orders) == 0:
            logger.error(f"Failed to find orders by backtest id: {backtest_id}")
            self._cancel_report(report_id=report["_id"])
            return

        report_id = report["_id"]
        allocation = snapshots[0]["allocation"]

        logger.info(f"Backtest id: {backtest_id}")
        logger.info(f"Report id: {report_id}")
        logger.info(f"Orders count: {len(orders)}")
        logger.info(f"Snapshots count: {len(snapshots)}")
        logger.info(f"Allocation: {allocation:,.2f}")

        self._perform_report(
            report,
            orders,
            snapshots,
        )

    # ───────────────────────────────────────────────────────────
    # PRIVATE METHODS
    # ───────────────────────────────────────────────────────────
    def _perform_report(
        self,
        report: Dict[str, Any],
        orders: List[Dict[str, Any]],
        snapshots: List[Dict[str, Any]],
    ) -> None:
        allocation = snapshots[0]["allocation"]
        report_id = report["_id"]

        (
            returns,
            performance,
            profits,
            cumulative_account_dates,
        ) = self._get_cumulative_returns_from_orders(
            orders=orders,
            allocation=allocation,
        )

        r2 = get_r2_from(performance)
        cagr = get_cagr_from(performance)
        calmar_ratio = get_calmar_ratio_from(performance)
        expected_shortfall = get_cvar_from(performance, cutoff=0.05)
        max_drawdown = get_max_drawdown_from(performance)
        profit_factor = get_profit_factor_from(profits)
        recovery_factor = get_recovery_factor_from(performance)
        sharpe_ratio = get_sharpe_ratio_from_orders(performance, risk_free_rate=0.0)
        sortino_ratio = get_sortino_ratio_from(performance)
        ulcer_index = get_ulcer_index_from(performance)

        self._store_returns(
            report_id=str(report_id),
            values=returns,
            dates=cumulative_account_dates,
        )

        self._store_performance(
            report_id=str(report_id),
            values=performance,
            dates=cumulative_account_dates,
        )

        self._update_report(
            report_id=report_id,
            data={
                "r2": r2,
                "cagr": cagr,
                "calmar_ratio": calmar_ratio,
                "expected_shortfall": expected_shortfall,
                "max_drawdown": max_drawdown,
                "profit_factor": profit_factor,
                "recovery_factor": recovery_factor,
                "sharpe_ratio": sharpe_ratio,
                "sortino_ratio": sortino_ratio,
                "ulcer_index": ulcer_index,
                "status": ReportStatus.READY.value,
            },
        )

    def _cancel_report(self, report_id: str) -> None:
        self._update_report(
            report_id=report_id,
            data={
                "status": ReportStatus.FAILED.value,
            },
        )

    def _get_backtest_by_id(self, backtest_id: str) -> Optional[Dict[str, Any]]:
        results = BacktestModel().find(
            query_filters={"_id": ObjectId(backtest_id)},
        )

        return results[0] if results else None

    def _get_cumulative_returns_from_orders(
        self,
        orders: List[Dict[str, Any]],
        allocation: float,
    ) -> Tuple[List[float], List[float], List[float], List[datetime]]:
        returns = []
        performance = []
        profits = []
        cumulative_account_dates = []
        total = 0.0

        for order in orders:
            total += order.get("profit", 0.0)
            returns.append(total)
            growth_pct = ((allocation + total) / allocation - 1) * 100
            performance.append(growth_pct)
            profits.append(order.get("profit", 0.0))
            cumulative_account_dates.append(order.get("created_at"))

        return (
            returns,
            performance,
            profits,
            cumulative_account_dates,
        )

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
        )

    def _get_snapshots_by_backtest_id(self, backtest_id: str) -> List[Dict[str, Any]]:
        return self._snapshot_model.find(
            limit=9**100,
            query_filters={"backtest_id": backtest_id},
        )

    def _update_report(self, report_id: str, data: Dict[str, Any]) -> None:
        self._report_model.update(
            query_filters={"_id": ObjectId(report_id)},
            data=data,
        )

    def _store_returns(
        self,
        report_id: str,
        values: List[float],
        dates: List[datetime],
    ) -> List[str]:
        documents = [
            {
                "report_id": report_id,
                "value": value,
                "date": date,
            }
            for value, date in zip(
                values,
                dates,
                strict=True,
            )
        ]
        return self._report_returns_model.store_many(data=documents)

    def _store_performance(
        self,
        report_id: str,
        values: List[float],
        dates: List[datetime],
    ) -> List[str]:
        documents = [
            {
                "report_id": report_id,
                "value": value,
                "date": date,
            }
            for value, date in zip(
                values,
                dates,
                strict=True,
            )
        ]
        return self._report_performances_model.store_many(data=documents)


@shared_task(name="apps.core.tasks.process_backtest")
def process_backtest(backtest_id: Optional[str] = None) -> Dict[str, Any]:
    task = ProcessBacktestTask()
    task.run(backtest_id=backtest_id)

    return {
        "status": "success",
        "time": datetime.now(tz=UTC),
    }
