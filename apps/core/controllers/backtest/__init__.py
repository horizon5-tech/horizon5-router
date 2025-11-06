import logging
from datetime import UTC, datetime
from typing import Any, ClassVar, Dict, List, Type

from bson import ObjectId
from cerberus import Validator
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request

from apps.core.authentication import APIKeyAuthentication
from apps.core.controllers.base import BaseController
from apps.core.enums.backtest_status import BacktestStatus
from apps.core.enums.http_status import HttpStatus
from apps.core.models.backtest import BacktestModel
from apps.core.tasks import make_backtest_report

from .schemas.delete import delete_schema
from .schemas.get import get_schema
from .schemas.post import post_schema
from .schemas.put import update_schema


class BacktestController(BaseController):
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
        self._model = BacktestModel()

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

        backtest_id = None
        backtest_data = dict(body)

        from_date = body.get("from_date", 0)
        from_date = float(from_date if from_date is not None else 0)
        backtest_data["from_date"] = datetime.fromtimestamp(from_date, tz=UTC)

        to_date = body.get("to_date", 0)
        to_date = float(to_date if to_date is not None else 0)
        backtest_data["to_date"] = datetime.fromtimestamp(to_date, tz=UTC)

        backtest_data["status"] = BacktestStatus.RUNNING.value

        try:
            backtest_id = self._model.store(data=backtest_data)

        except Exception as e:
            logger.error(f"Failed to create backtest: {e}")

        if not backtest_id:
            return self.response(
                success=False,
                message="Failed to create backtest",
                status=HttpStatus.INTERNAL_SERVER_ERROR,
            )

        return self.response(
            success=True,
            message="Backtest created successfully",
            data={"_id": backtest_id},
            status=HttpStatus.OK,
        )

    @extend_schema(**update_schema())
    def put(self, request: Request, id: str) -> JsonResponse:
        logger = logging.getLogger("django")
        data = getattr(request, "data", {})
        body = data if isinstance(data, dict) else {}
        backtest = None

        if not self._is_update_data_valid(body):
            return self.response(
                success=False,
                message="Invalid request data",
                status=HttpStatus.BAD_REQUEST,
            )

        try:
            backtest = self._model.find(
                query_filters={
                    "_id": ObjectId(id),
                }
            )[0]
        except Exception as e:
            logger.error(f"Failed to find backtest: {e}")

            return self.response(
                success=False,
                message="Failed to find backtest",
                status=HttpStatus.INTERNAL_SERVER_ERROR,
            )

        if not backtest:
            return self.response(
                success=False,
                message="Backtest not found",
                status=HttpStatus.NOT_FOUND,
            )

        to_update = {}
        previous_status = backtest.get("status")
        new_status = body.get("status")

        if "asset" in body:
            to_update["asset"] = body.get("asset")

        if "start_at" in body:
            start_at = body.get("start_at")
            start_at = float(start_at if start_at is not None else 0)
            start_at = datetime.fromtimestamp(start_at, tz=UTC)
            to_update["start_at"] = start_at

        if "end_at" in body:
            end_at = body.get("end_at")
            end_at = float(end_at if end_at is not None else 0)
            end_at = datetime.fromtimestamp(end_at, tz=UTC)
            to_update["end_at"] = end_at

        if "status" in body:
            to_update["status"] = body.get("status")

        try:
            self._model.update(
                query_filters={"_id": ObjectId(id)},
                data=to_update,
            )
        except Exception as e:
            logger.error(f"Failed to update backtest: {e}")

        if (
            previous_status == BacktestStatus.RUNNING.value
            and new_status == BacktestStatus.COMPLETED.value
        ):
            try:
                make_backtest_report.apply_async(
                    args=[str(id)],
                    countdown=10,
                )  # type: ignore
            except Exception as e:
                logger.error(f"Failed to trigger make_backtest_report task: {e}")

        return self.response(
            success=True,
            message="Backtest updated successfully",
            data={},
            status=HttpStatus.OK,
        )

    @extend_schema(**delete_schema())
    def delete(self, request: Request, id: str) -> JsonResponse:
        logger = logging.getLogger("django")
        backtest = None

        try:
            results = self._model.find(
                query_filters={
                    "_id": ObjectId(id),
                }
            )
            backtest = results[0] if results else None
        except Exception as e:
            logger.error(f"Failed to find backtest: {e}")

            return self.response(
                success=False,
                message="Failed to find backtest",
                status=HttpStatus.INTERNAL_SERVER_ERROR,
            )

        if not backtest:
            return self.response(
                success=False,
                message="Backtest not found",
                status=HttpStatus.NOT_FOUND,
            )

        try:
            self._model.delete(
                query_filters={
                    "_id": ObjectId(id),
                }
            )
        except Exception as e:
            logger.error(f"Failed to delete backtest: {e}")

            return self.response(
                success=False,
                message="Failed to delete backtest",
                status=HttpStatus.INTERNAL_SERVER_ERROR,
            )

        return self.response(
            success=True,
            message="Backtest deleted successfully",
            status=HttpStatus.OK,
        )

    # ───────────────────────────────────────────────────────────
    # PRIVATE METHODS
    # ───────────────────────────────────────────────────────────
    def _is_post_data_valid(self, body: Dict[str, Any]) -> bool:
        validator = Validator(
            {
                "asset": {
                    "type": "string",
                    "required": True,
                    "minlength": 1,
                },
                "strategies": {
                    "type": "string",
                    "required": True,
                    "minlength": 1,
                },
                "from_date": {
                    "type": "integer",
                    "required": True,
                    "coerce": int,
                },
                "to_date": {
                    "type": "integer",
                    "required": True,
                    "coerce": int,
                },
            }  # type: ignore
        )

        return validator.validate(body)  # type: ignore

    def _is_update_data_valid(self, body: Dict[str, Any]) -> bool:
        validator = Validator(
            {
                "status": {  # type: ignore
                    "type": "string",
                    "required": False,
                    "allowed": [s.value for s in BacktestStatus],
                },
            },
            allow_unknown=True,
        )

        return validator.validate(body)  # type: ignore
