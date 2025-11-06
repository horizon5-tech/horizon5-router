from typing import Any

from drf_spectacular.utils import inline_serializer
from rest_framework import serializers


def post_schema() -> Any:
    return {
        "tags": ["Backtest"],
        "summary": "Create a backtest",
        "description": "Creates a new backtest record in the database.",
        "request": inline_serializer(
            name="BacktestRequest",
            fields={
                "asset": serializers.CharField(),
                "strategies": serializers.CharField(),
                "from_date": serializers.IntegerField(),
                "to_date": serializers.IntegerField(),
            },
        ),
        "responses": {
            201: inline_serializer(
                name="BacktestResponse",
                fields={
                    "success": serializers.BooleanField(),
                    "message": serializers.CharField(),
                    "data": inline_serializer(
                        name="BacktestData",
                        fields={
                            "success": serializers.BooleanField(),
                        },
                    ),
                },
            ),
        },
    }
