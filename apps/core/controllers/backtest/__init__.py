from typing import Any, ClassVar, List, Type

from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request

from apps.core.authentication import APIKeyAuthentication
from apps.core.controllers.base import BaseController
from apps.core.models.backtest import BacktestModel

from .schemas.get import get_schema


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
