from apps.core.models.base import BaseModel
from apps.core.repositories.snapshot import SnapshotRepository


class SnapshotModel(BaseModel):
    def __init__(self) -> None:
        super().__init__()
        self._repository = SnapshotRepository()
