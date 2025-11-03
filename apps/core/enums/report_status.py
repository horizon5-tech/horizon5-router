from enum import Enum


class ReportStatus(Enum):
    BUILDING = "building"
    READY = "ready"
    FAILED = "failed"
