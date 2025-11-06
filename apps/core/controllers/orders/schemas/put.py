from typing import Any

from drf_spectacular.utils import OpenApiParameter, inline_serializer
from rest_framework import serializers


def update_schema() -> Any:
    return {
        "tags": ["Order"],
        "summary": "Update an order",
        "description": (
            "Updates an existing order record in the database. "
            "All fields are optional - only include the fields you want to update."
        ),
        "parameters": [
            OpenApiParameter(
                name="id",
                type=str,
                location=OpenApiParameter.PATH,
                description="Order ID",
                required=True,
            ),
        ],
        "request": inline_serializer(
            name="OrderUpdateRequest",
            fields={
                "backtest": serializers.BooleanField(required=False),
                "strategy_id": serializers.CharField(required=False),
                "symbol": serializers.CharField(required=False),
                "gateway": serializers.CharField(required=False),
                "side": serializers.CharField(required=False),
                "order_type": serializers.CharField(required=False),
                "status": serializers.CharField(required=False),
                "volume": serializers.FloatField(required=False),
                "executed_volume": serializers.FloatField(required=False),
                "price": serializers.FloatField(required=False),
                "filled": serializers.BooleanField(required=False),
                "created_at": serializers.IntegerField(required=False),
                "updated_at": serializers.IntegerField(required=False),
                "backtest_id": serializers.CharField(required=False),
                "close_price": serializers.FloatField(required=False),
                "take_profit_price": serializers.FloatField(required=False),
                "stop_loss_price": serializers.FloatField(required=False),
                "client_order_id": serializers.CharField(required=False),
                "profit": serializers.FloatField(required=False),
                "profit_percentage": serializers.FloatField(required=False),
            },
        ),
        "responses": {
            200: inline_serializer(
                name="OrderUpdateResponse",
                fields={
                    "success": serializers.BooleanField(),
                    "message": serializers.CharField(),
                },
            ),
        },
    }
