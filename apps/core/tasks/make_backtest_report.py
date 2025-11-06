from datetime import UTC, datetime
from typing import Any, Dict, Optional

from celery import shared_task

from apps.core.tasks.backtest.report import BacktestReportTask


@shared_task(name="apps.core.tasks.make_backtest_report")
def make_backtest_report(backtest_id: Optional[str] = None) -> Dict[str, Any]:
    task = BacktestReportTask()
    task.run(backtest_id=backtest_id)

    return {
        "status": "success",
        "time": datetime.now(tz=UTC),
    }
