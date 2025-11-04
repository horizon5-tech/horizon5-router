from typing import Any

from drf_spectacular.utils import OpenApiExample, OpenApiParameter, inline_serializer
from rest_framework import serializers


def update_schema() -> Any:
    return {
        "tags": ["Backtest"],
        "summary": "Update a backtest",
        "description": (
            "Updates an existing backtest record in the database. "
            "All fields are optional - only include the fields you want to update."
        ),
        "parameters": [
            OpenApiParameter(
                name="id",
                type=str,
                location=OpenApiParameter.PATH,
                description="Backtest ID",
                required=True,
            ),
        ],
        "request": inline_serializer(
            name="BacktestUpdateRequest",
            fields={
                "asset": serializers.CharField(
                    required=False,
                    default="{btcusdt}",
                ),
                "start_at": serializers.IntegerField(
                    required=False,
                    default="{timestamp}",
                ),
                "end_at": serializers.IntegerField(
                    required=False,
                    default="{timestamp}",
                ),
                "status": serializers.ChoiceField(
                    choices=["pending", "running", "completed", "failed"],
                    required=False,
                    default="{running}",
                ),
            },
        ),
        "responses": {
            200: inline_serializer(
                name="BacktestUpdateResponse",
                fields={
                    "success": serializers.BooleanField(),
                },
            ),
        },
    }
