import logging
from datetime import UTC, datetime
from typing import Any, ClassVar, Dict, List, Type

from cerberus import Validator
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request

from apps.core.authentication import APIKeyAuthentication
from apps.core.controllers.base import BaseController
from apps.core.enums.http_status import HttpStatus
from apps.core.models.snapshot import SnapshotModel

from .schemas.get import get_schema
from .schemas.post import post_schema


class SnapshotController(BaseController):
    # ───────────────────────────────────────────────────────────
    # PROPERTIES
    # ───────────────────────────────────────────────────────────
    authentication_classes: ClassVar[List[Type[BaseAuthentication]]] = [
        APIKeyAuthentication
    ]

    # ───────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._model = SnapshotModel()

    # ───────────────────────────────────────────────────────────
    # PUBLIC METHODS
    # ───────────────────────────────────────────────────────────
    @extend_schema(**get_schema())
    def get(self, request: Request) -> JsonResponse:
        return super().get(request)

    @extend_schema(**post_schema())
    def post(self, request: Request) -> JsonResponse:
        logger = logging.getLogger("django")
        data = getattr(request, "data", {})
        body = data if isinstance(data, dict) else {}

        if not self._is_post_data_valid(body):
            return self.response(
                success=False,
                message="Invalid request data",
                status=HttpStatus.BAD_REQUEST,
            )

        snapshot_id = None

        session_id = body.get("session_id")
        event = body.get("event")
        date = body.get("date", 0)
        date = float(date if date is not None else 0)
        date = datetime.fromtimestamp(date, tz=UTC)

        nav = body.get("nav", 0)
        nav = float(nav if nav is not None else 0)

        allocation = body.get("allocation", 0)
        allocation = float(allocation if allocation is not None else 0)

        nav_peak = body.get("nav_peak", 0)
        nav_peak = float(nav_peak if nav_peak is not None else 0)

        try:
            snapshot_id = self._model.store(
                data={
                    "session_id": session_id,
                    "event": event,
                    "date": date,
                    "nav": nav,
                    "nav_peak": nav_peak,
                    "allocation": allocation,
                }
            )

        except Exception as e:
            logger.error(f"Failed to create snapshot: {e}")

        if not snapshot_id:
            return self.response(
                success=False,
                message="Failed to create snapshot",
                status=HttpStatus.INTERNAL_SERVER_ERROR,
            )

        return self.response(
            success=True,
            message="Snapshot created successfully",
            data={"_id": snapshot_id},
            status=HttpStatus.OK,
        )

    # ───────────────────────────────────────────────────────────
    # PRIVATE METHODS
    # ───────────────────────────────────────────────────────────
    def _is_post_data_valid(self, body: Dict[str, Any]) -> bool:
        validator = Validator(
            {
                "session_id": {
                    "type": "integer",
                    "required": True,
                    "coerce": int,
                },
                "event": {
                    "type": "string",
                    "required": True,
                    "minlength": 1,
                },
                "date": {
                    "type": "integer",
                    "required": True,
                    "coerce": int,
                },
                "nav": {
                    "type": "float",
                    "required": True,
                    "coerce": float,
                },
                "allocation": {
                    "type": "float",
                    "required": True,
                    "coerce": float,
                },
                "nav_peak": {
                    "type": "float",
                    "required": True,
                    "coerce": float,
                },
            }  # type: ignore
        )

        return validator.validate(body)  # type: ignore
