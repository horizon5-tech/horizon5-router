from typing import Any

from drf_spectacular.utils import OpenApiParameter, inline_serializer
from rest_framework import serializers


def delete_schema() -> Any:
    return {
        "tags": ["Backtest"],
        "summary": "Delete a backtest",
        "description": (
            "Deletes an existing backtest record from the database. "
            "This operation cannot be undone."
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
        "responses": {
            200: inline_serializer(
                name="BacktestDeleteResponse",
                fields={
                    "success": serializers.BooleanField(),
                    "message": serializers.CharField(),
                },
            ),
            404: inline_serializer(
                name="BacktestNotFoundResponse",
                fields={
                    "success": serializers.BooleanField(),
                    "message": serializers.CharField(),
                },
            ),
        },
    }
