import logging
from datetime import UTC, datetime
from typing import Any, ClassVar, Dict, List, Optional, Type

from bson import ObjectId
from cerberus import Validator
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request

from apps.core.authentication import APIKeyAuthentication
from apps.core.controllers.base import BaseController
from apps.core.enums.http_status import HttpStatus
from apps.core.models.snapshot import SnapshotModel

from .schemas.delete import delete_schema
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

        validation_errors = self._is_post_data_valid(body)
        if validation_errors:
            return self.response(
                success=False,
                message="Invalid request data",
                data={"errors": validation_errors},
                status=HttpStatus.BAD_REQUEST,
            )

        snapshot_id = None
        snapshot_data = dict(body)

        if "created_at" in body:
            created_at = body.get("created_at", 0)
            created_at = float(created_at if created_at is not None else 0)
            snapshot_data["created_at"] = datetime.fromtimestamp(created_at, tz=UTC)

        try:
            snapshot_id = self._model.store(data=snapshot_data)

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

    @extend_schema(**delete_schema())
    def delete(self, request: Request, id: str) -> JsonResponse:
        logger = logging.getLogger("django")
        snapshot = None

        try:
            results = self._model.find(
                query_filters={
                    "_id": ObjectId(id),
                }
            )

            snapshot = results[0] if results else None
        except Exception as e:
            logger.error(f"Failed to find snapshot: {e}")

            return self.response(
                success=False,
                message="Failed to find snapshot",
                status=HttpStatus.INTERNAL_SERVER_ERROR,
            )

        if not snapshot:
            return self.response(
                success=False,
                message="Snapshot not found",
                status=HttpStatus.NOT_FOUND,
            )

        try:
            self._model.delete(
                query_filters={
                    "_id": ObjectId(id),
                }
            )
        except Exception as e:
            logger.error(f"Failed to delete snapshot: {e}")

            return self.response(
                success=False,
                message="Failed to delete snapshot",
                status=HttpStatus.INTERNAL_SERVER_ERROR,
            )

        return self.response(
            success=True,
            message="Snapshot deleted successfully",
            status=HttpStatus.OK,
        )

    # ───────────────────────────────────────────────────────────
    # PRIVATE METHODS
    # ───────────────────────────────────────────────────────────
    def _is_post_data_valid(self, body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        validator = Validator(
            {
                "backtest_id": {
                    "type": "string",
                    "required": True,
                    "minlength": 1,
                },
                "backtest": {
                    "type": "boolean",
                    "required": True,
                    "coerce": bool,
                },
                "strategy_id": {
                    "type": "string",
                    "required": True,
                    "minlength": 1,
                },
                "event": {
                    "type": "string",
                    "required": False,
                    "nullable": True,
                },
                "nav": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                    "min": 0,
                },
                "allocation": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                    "min": 0,
                },
                "nav_peak": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                    "min": 0,
                },
                "r2": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                    "min": 0,
                    "max": 1,
                },
                "cagr": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                },
                "calmar_ratio": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                },
                "expected_shortfall": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                },
                "max_drawdown": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                    "max": 0,
                },
                "profit_factor": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                    "min": 0,
                },
                "recovery_factor": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                },
                "sharpe_ratio": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                },
                "sortino_ratio": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                },
                "ulcer_index": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                    "min": 0,
                },
                "created_at": {
                    "type": "integer",
                    "required": False,
                    "nullable": True,
                    "coerce": int,
                },
            }  # type: ignore
        )

        is_valid = validator.validate(body)  # type: ignore

        if not is_valid:
            return validator.errors  # type: ignore

        return None
