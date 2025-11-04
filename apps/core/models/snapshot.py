from datetime import UTC, datetime
from typing import Any, Dict

from apps.core.models.base import BaseModel
from apps.core.repositories.snapshot import SnapshotRepository


class SnapshotModel(BaseModel):
    # ───────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────
    def __init__(self) -> None:
        super().__init__()
        self._repository = SnapshotRepository()

    # ───────────────────────────────────────────────────────────
    # PUBLIC METHODS
    # ───────────────────────────────────────────────────────────
    def store(
        self,
        data: Dict[str, Any],
    ) -> str:
        now = datetime.now(tz=UTC)
        data["created_at"] = now
        data["updated_at"] = now
        return self._repository.store(data=data)
