from datetime import UTC, datetime
from typing import Any

from celery import shared_task

from apps.core.models.backtest import BacktestModel
from apps.core.models.report import ReportModel
from apps.core.services.logging import LoggingService


class ProcessBacktestsTask:
    _name: str = "process_backtests"

    def __init__(self) -> None:
        self._logger = LoggingService()
        self._logger.setup(self._name)

        self._backtest_model = BacktestModel()
        self._report_model = ReportModel()

    def run(self) -> None:
        self._logger.info(f"Processing task: {self._name}")


@shared_task(name="apps.core.tasks.process_backtests")
def process_backtests() -> dict[str, Any]:
    task = ProcessBacktestsTask()
    task.run()

    return {"status": "success", "time": datetime.now(tz=UTC)}
