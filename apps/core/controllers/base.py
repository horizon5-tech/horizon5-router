from datetime import datetime
from typing import Any, Dict, List, Optional

from bson import ObjectId
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.core.enums.http_status import HttpStatus
from apps.core.models.base import BaseModel


class BaseController(APIView):
    # ───────────────────────────────────────────────────────────
    # PROPERTIES
    # ───────────────────────────────────────────────────────────
    _model: BaseModel

    # ───────────────────────────────────────────────────────────
    # PUBLIC METHODS
    # ───────────────────────────────────────────────────────────
    def get(self, request: Request) -> JsonResponse:
        response = {}
        query_params = request.query_params

        page_param = query_params.get("page", "1")
        page_size_param = query_params.get("page_size", "10")
        sort_by_param = query_params.get("sort", "created_at")
        sort_direction_param = query_params.get("sort_order", "desc")

        page = int(page_param)  # type: ignore
        page_size = int(page_size_param)  # type: ignore
        sort_by = str(sort_by_param)  # type: ignore
        sort_direction = str(sort_direction_param)  # type: ignore

        limit = int(page_size)
        offset = (page - 1) * limit

        try:
            results = self._model.find(
                limit=limit,
                offset=offset,
                sort_by=sort_by,
                sort_direction=sort_direction,
            )
            response["results"] = [self._serialize(doc) for doc in results]
        except Exception as e:
            return self.response(
                success=False,
                message=str(e),
                status=HttpStatus.INTERNAL_SERVER_ERROR,
            )

        return self.response(
            success=True,
            message="Data retrieved successfully",
            data=response,
            status=HttpStatus.OK,
        )

    def response(
        self,
        success: bool,
        message: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        status: Optional[HttpStatus] = None,
    ) -> JsonResponse:
        response_code = HttpStatus.OK.value if success else HttpStatus.BAD_REQUEST.value
        response: Dict[str, Any] = {
            "success": success,
        }

        if message is not None:
            response["message"] = message

        if data is not None:
            response["data"] = data

        return JsonResponse(
            response,
            status=response_code if status is None else status.value,
        )

    # ───────────────────────────────────────────────────────────
    # PRIVATE METHODS
    # ───────────────────────────────────────────────────────────
    def _serialize(self, document: Dict[str, Any]) -> Dict[str, Any]:
        serialized = {}

        for key, value in document.items():
            if isinstance(value, ObjectId):
                serialized[key] = str(value)

            elif isinstance(value, datetime):
                serialized[key] = value.isoformat()

            elif isinstance(value, dict):
                serialized[key] = self._serialize(value)

            elif isinstance(value, list):
                serialized[key] = [
                    self._serialize(item) if isinstance(item, dict) else item
                    for item in value
                ]

            else:
                serialized[key] = value

        return serialized
