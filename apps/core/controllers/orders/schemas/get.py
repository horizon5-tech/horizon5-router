from typing import Any

from drf_spectacular.utils import inline_serializer
from rest_framework import serializers

from apps.core.schemas.pagination import pagination_schema
from apps.core.schemas.responses import response_200_schema


def get_schema() -> Any:
    return {
        "tags": ["Order"],
        "summary": "Get orders",
        "description": (
            "Provides a list of orders saved on the database, "
            "and also allows to filter the results by various parameters."
        ),
        "parameters": [
            *pagination_schema(),
        ],
        "responses": {
            **response_200_schema(
                "OrderController",
                {
                    "data": inline_serializer(
                        name="Orders",
                        fields={
                            "id": serializers.CharField(),
                            "gateway_order_id": serializers.CharField(
                                required=False, allow_null=True
                            ),
                            "backtest": serializers.BooleanField(),
                            "backtest_id": serializers.CharField(
                                required=False, allow_null=True
                            ),
                            "portfolio_id": serializers.CharField(
                                required=False, allow_null=True
                            ),
                            "asset_id": serializers.CharField(
                                required=False, allow_null=True
                            ),
                            "strategy_id": serializers.CharField(),
                            "symbol": serializers.CharField(),
                            "gateway": serializers.CharField(),
                            "side": serializers.CharField(),
                            "order_type": serializers.CharField(),
                            "status": serializers.CharField(),
                            "volume": serializers.FloatField(),
                            "executed_volume": serializers.FloatField(),
                            "price": serializers.FloatField(),
                            "close_price": serializers.FloatField(
                                required=False, allow_null=True
                            ),
                            "take_profit_price": serializers.FloatField(
                                required=False, allow_null=True
                            ),
                            "stop_loss_price": serializers.FloatField(
                                required=False, allow_null=True
                            ),
                            "commission": serializers.FloatField(
                                required=False, allow_null=True
                            ),
                            "commission_percentage": serializers.FloatField(
                                required=False, allow_null=True
                            ),
                            "client_order_id": serializers.CharField(
                                required=False, allow_null=True
                            ),
                            "filled": serializers.BooleanField(),
                            "profit": serializers.FloatField(
                                required=False, allow_null=True
                            ),
                            "profit_percentage": serializers.FloatField(
                                required=False, allow_null=True
                            ),
                            "trades": serializers.ListField(
                                required=False, allow_null=True
                            ),
                            "logs": serializers.ListField(
                                required=False, allow_null=True
                            ),
                            "variables": serializers.DictField(
                                required=False, allow_null=True
                            ),
                            "created_at": serializers.DateTimeField(),
                            "updated_at": serializers.DateTimeField(),
                        },
                    ),
                },
            ),
        },
    }
