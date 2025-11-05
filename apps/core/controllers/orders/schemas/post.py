from typing import Any

from drf_spectacular.utils import inline_serializer
from rest_framework import serializers


def post_schema() -> Any:
    return {
        "tags": ["Order"],
        "summary": "Create an order",
        "description": "Creates a new order record in the database.",
        "request": inline_serializer(
            name="OrderRequest",
            fields={
                "backtest": serializers.BooleanField(),
                "backtest_id": serializers.CharField(required=False, allow_null=True),
                "source": serializers.CharField(),
                "symbol": serializers.CharField(),
                "gateway": serializers.CharField(),
                "side": serializers.CharField(),
                "order_type": serializers.CharField(),
                "status": serializers.CharField(),
                "volume": serializers.FloatField(),
                "executed_volume": serializers.FloatField(),
                "price": serializers.FloatField(),
                "close_price": serializers.FloatField(required=False, allow_null=True),
                "take_profit_price": serializers.FloatField(
                    required=False, allow_null=True
                ),
                "stop_loss_price": serializers.FloatField(
                    required=False, allow_null=True
                ),
                "client_order_id": serializers.CharField(
                    required=False, allow_null=True
                ),
                "filled": serializers.BooleanField(),
                "profit": serializers.FloatField(required=False, allow_null=True),
                "profit_percentage": serializers.FloatField(
                    required=False, allow_null=True
                ),
                "created_at": serializers.IntegerField(),
                "updated_at": serializers.IntegerField(),
            },
        ),
        "responses": {
            201: inline_serializer(
                name="OrderResponse",
                fields={
                    "success": serializers.BooleanField(),
                    "message": serializers.CharField(),
                    "data": inline_serializer(
                        name="OrderData",
                        fields={
                            "_id": serializers.CharField(),
                        },
                    ),
                },
            ),
        },
    }
