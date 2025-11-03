from typing import Any, Dict, List

from apps.core.models.backtest import BacktestModel
from apps.core.models.base import BaseModel
from apps.core.repositories.report import ReportRepository


class ReportModel(BaseModel):
    # ───────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────
    def __init__(self) -> None:
        super().__init__()
        self._repository = ReportRepository()

    def get_backtests_by_report_id(self, report_id: str) -> List[Dict[str, Any]]:
        backtest_model = BacktestModel()

        return backtest_model.find(
            query_filters={"report_id": report_id},
        )
