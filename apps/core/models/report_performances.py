from apps.core.models.base import BaseModel
from apps.core.repositories.report_performances import ReportPerformancesRepository


class ReportPerformancesModel(BaseModel):
    # ───────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────
    def __init__(self) -> None:
        super().__init__()
        self._repository = ReportPerformancesRepository()
