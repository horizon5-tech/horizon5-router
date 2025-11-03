from apps.core.repositories.base import BaseRepository


class SnapshotRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(collection_name="snapshots")
