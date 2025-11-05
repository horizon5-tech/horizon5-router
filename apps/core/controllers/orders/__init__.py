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
from apps.core.enums.http_status import HttpStatus
from apps.core.models.order import OrderModel

from .schemas.delete import delete_schema
from .schemas.get import get_schema
from .schemas.post import post_schema
from .schemas.put import update_schema


class OrderController(BaseController):
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
        self._model = OrderModel()

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

        created_at = body.get("created_at", 0)
        created_at = float(created_at if created_at is not None else 0)
        created_at = datetime.fromtimestamp(created_at, tz=UTC)

        updated_at = body.get("updated_at", 0)
        updated_at = float(updated_at if updated_at is not None else 0)
        updated_at = datetime.fromtimestamp(updated_at, tz=UTC)

        order = {
            "backtest": body.get("backtest"),
            "source": body.get("source"),
            "symbol": body.get("symbol"),
            "gateway": body.get("gateway"),
            "side": body.get("side"),
            "order_type": body.get("order_type"),
            "status": body.get("status"),
            "volume": body.get("volume"),
            "executed_volume": body.get("executed_volume"),
            "price": body.get("price"),
            "filled": body.get("filled"),
            "created_at": created_at,
            "updated_at": updated_at,
        }

        if "backtest_id" in body and body.get("backtest_id") is not None:
            order["backtest_id"] = body.get("backtest_id")

        if "close_price" in body and body.get("close_price") is not None:
            order["close_price"] = body.get("close_price")

        if "take_profit_price" in body and body.get("take_profit_price") is not None:
            order["take_profit_price"] = body.get("take_profit_price")

        if "stop_loss_price" in body and body.get("stop_loss_price") is not None:
            order["stop_loss_price"] = body.get("stop_loss_price")

        if "client_order_id" in body and body.get("client_order_id") is not None:
            order["client_order_id"] = body.get("client_order_id")

        if "profit" in body and body.get("profit") is not None:
            order["profit"] = body.get("profit")

        if "profit_percentage" in body and body.get("profit_percentage") is not None:
            order["profit_percentage"] = body.get("profit_percentage")

        order_id = None

        try:
            order_id = self._model.store(data=order)
        except Exception as e:
            logger.error(f"Failed to create order: {e}")

        if not order_id:
            return self.response(
                success=False,
                message="Failed to create order",
                status=HttpStatus.INTERNAL_SERVER_ERROR,
            )

        return self.response(
            success=True,
            message="Order created successfully",
            data={"_id": order_id},
            status=HttpStatus.CREATED,
        )

    @extend_schema(**update_schema())
    def put(self, request: Request, id: str) -> JsonResponse:
        logger = logging.getLogger("django")
        data = getattr(request, "data", {})
        body = data if isinstance(data, dict) else {}
        order = None

        if not self._is_update_data_valid(body):
            return self.response(
                success=False,
                message="Invalid request data",
                status=HttpStatus.BAD_REQUEST,
            )

        try:
            results = self._model.find(
                query_filters={
                    "_id": ObjectId(id),
                }
            )
            order = results[0] if results else None
        except Exception as e:
            logger.error(f"Failed to find order: {e}")

            return self.response(
                success=False,
                message="Failed to find order",
                status=HttpStatus.INTERNAL_SERVER_ERROR,
            )

        if not order:
            return self.response(
                success=False,
                message="Order not found",
                status=HttpStatus.NOT_FOUND,
            )

        to_update = {}

        if "backtest" in body:
            to_update["backtest"] = body.get("backtest")

        if "source" in body:
            to_update["source"] = body.get("source")

        if "symbol" in body:
            to_update["symbol"] = body.get("symbol")

        if "gateway" in body:
            to_update["gateway"] = body.get("gateway")

        if "side" in body:
            to_update["side"] = body.get("side")

        if "order_type" in body:
            to_update["order_type"] = body.get("order_type")

        if "status" in body:
            to_update["status"] = body.get("status")

        if "volume" in body:
            volume = body.get("volume")
            if volume is not None:
                to_update["volume"] = float(volume)

        if "executed_volume" in body:
            executed_volume = body.get("executed_volume")
            if executed_volume is not None:
                to_update["executed_volume"] = float(executed_volume)

        if "price" in body:
            price = body.get("price")
            if price is not None:
                to_update["price"] = float(price)

        if "filled" in body:
            to_update["filled"] = body.get("filled")

        if "created_at" in body:
            created_at = body.get("created_at")
            created_at = float(created_at if created_at is not None else 0)
            created_at = datetime.fromtimestamp(created_at, tz=UTC)
            to_update["created_at"] = created_at

        if "updated_at" in body:
            updated_at = body.get("updated_at")
            updated_at = float(updated_at if updated_at is not None else 0)
            updated_at = datetime.fromtimestamp(updated_at, tz=UTC)
            to_update["updated_at"] = updated_at

        if "backtest_id" in body and body.get("backtest_id") is not None:
            to_update["backtest_id"] = body.get("backtest_id")

        if "close_price" in body:
            close_price = body.get("close_price")
            if close_price is not None:
                to_update["close_price"] = float(close_price)

        if "take_profit_price" in body:
            take_profit_price = body.get("take_profit_price")
            if take_profit_price is not None:
                to_update["take_profit_price"] = float(take_profit_price)

        if "stop_loss_price" in body:
            stop_loss_price = body.get("stop_loss_price")
            if stop_loss_price is not None:
                to_update["stop_loss_price"] = float(stop_loss_price)

        if "client_order_id" in body and body.get("client_order_id") is not None:
            to_update["client_order_id"] = body.get("client_order_id")

        if "profit" in body:
            profit = body.get("profit")
            if profit is not None:
                to_update["profit"] = float(profit)

        if "profit_percentage" in body:
            profit_percentage = body.get("profit_percentage")
            if profit_percentage is not None:
                to_update["profit_percentage"] = float(profit_percentage)

        try:
            self._model.update(
                query_filters={"_id": ObjectId(id)},
                data=to_update,
            )
        except Exception as e:
            logger.error(f"Failed to update order: {e}")

            return self.response(
                success=False,
                message="Failed to update order",
                status=HttpStatus.INTERNAL_SERVER_ERROR,
            )

        return self.response(
            success=True,
            message="Order updated successfully",
            data={},
            status=HttpStatus.OK,
        )

    @extend_schema(**delete_schema())
    def delete(self, request: Request, id: str) -> JsonResponse:
        logger = logging.getLogger("django")
        order = None

        try:
            results = self._model.find(
                query_filters={
                    "_id": ObjectId(id),
                }
            )

            order = results[0] if results else None
        except Exception as e:
            logger.error(f"Failed to find order: {e}")

            return self.response(
                success=False,
                message="Failed to find order",
                status=HttpStatus.INTERNAL_SERVER_ERROR,
            )

        if not order:
            return self.response(
                success=False,
                message="Order not found",
                status=HttpStatus.NOT_FOUND,
            )

        try:
            self._model.delete(
                query_filters={
                    "_id": ObjectId(id),
                }
            )

        except Exception as e:
            logger.error(f"Failed to delete order: {e}")

            return self.response(
                success=False,
                message="Failed to delete order",
                status=HttpStatus.INTERNAL_SERVER_ERROR,
            )

        return self.response(
            success=True,
            message="Order deleted successfully",
            status=HttpStatus.OK,
        )

    # ───────────────────────────────────────────────────────────
    # PRIVATE METHODS
    # ───────────────────────────────────────────────────────────
    def _is_post_data_valid(self, body: Dict[str, Any]) -> bool:
        validator = Validator(
            {
                "backtest": {
                    "type": "boolean",
                    "required": True,
                },
                "backtest_id": {
                    "type": "string",
                    "required": False,
                    "nullable": True,
                },
                "source": {
                    "type": "string",
                    "required": True,
                    "minlength": 1,
                },
                "symbol": {
                    "type": "string",
                    "required": True,
                    "minlength": 1,
                },
                "gateway": {
                    "type": "string",
                    "required": True,
                    "minlength": 1,
                },
                "side": {
                    "type": "string",
                    "required": True,
                    "allowed": ["buy", "sell"],
                },
                "order_type": {
                    "type": "string",
                    "required": True,
                    "minlength": 1,
                },
                "status": {
                    "type": "string",
                    "required": True,
                    "minlength": 1,
                },
                "volume": {
                    "type": "float",
                    "required": True,
                    "coerce": float,
                },
                "executed_volume": {
                    "type": "float",
                    "required": True,
                    "coerce": float,
                },
                "price": {
                    "type": "float",
                    "required": True,
                    "coerce": float,
                },
                "close_price": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                },
                "take_profit_price": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                },
                "stop_loss_price": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                },
                "client_order_id": {
                    "type": "string",
                    "required": False,
                    "nullable": True,
                },
                "filled": {
                    "type": "boolean",
                    "required": True,
                },
                "profit": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                },
                "profit_percentage": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                },
                "created_at": {
                    "type": "integer",
                    "required": True,
                    "coerce": int,
                },
                "updated_at": {
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
                "backtest": {
                    "type": "boolean",
                    "required": False,
                },
                "source": {
                    "type": "string",
                    "required": False,
                    "minlength": 1,
                },
                "symbol": {
                    "type": "string",
                    "required": False,
                    "minlength": 1,
                },
                "gateway": {
                    "type": "string",
                    "required": False,
                    "minlength": 1,
                },
                "side": {
                    "type": "string",
                    "required": False,
                    "allowed": ["buy", "sell"],
                },
                "order_type": {
                    "type": "string",
                    "required": False,
                    "minlength": 1,
                },
                "status": {
                    "type": "string",
                    "required": False,
                    "minlength": 1,
                },
                "volume": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                },
                "executed_volume": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                },
                "price": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                },
                "filled": {
                    "type": "boolean",
                    "required": False,
                },
                "created_at": {
                    "type": "integer",
                    "required": False,
                    "coerce": int,
                },
                "updated_at": {
                    "type": "integer",
                    "required": False,
                    "coerce": int,
                },
                "backtest_id": {
                    "type": "string",
                    "required": False,
                    "nullable": True,
                },
                "close_price": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                },
                "take_profit_price": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                },
                "stop_loss_price": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                },
                "client_order_id": {
                    "type": "string",
                    "required": False,
                    "nullable": True,
                },
                "profit": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                },
                "profit_percentage": {
                    "type": "float",
                    "required": False,
                    "nullable": True,
                    "coerce": float,
                },
            },  # type: ignore
            allow_unknown=True,
        )

        return validator.validate(body)  # type: ignore
