from apps.core.repositories.base import BaseRepository


class ReportReturnsRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(collection_name="report_returns")

