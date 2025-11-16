from typing import Any

from drf_spectacular.utils import inline_serializer
from rest_framework import serializers


def post_schema() -> Any:
    return {
        "tags": ["Snapshot"],
        "summary": "Create a snapshot",
        "description": "Creates a new snapshot record in the database.",
        "request": inline_serializer(
            name="SnapshotRequest",
            fields={
                "backtest": serializers.BooleanField(),
                "backtest_id": serializers.CharField(required=False, allow_null=True),
                "strategy_id": serializers.CharField(),
                "event": serializers.CharField(required=False),
                "nav": serializers.FloatField(required=False),
                "allocation": serializers.FloatField(required=False),
                "nav_peak": serializers.FloatField(required=False),
                "r2": serializers.FloatField(required=False),
                "cagr": serializers.FloatField(required=False),
                "calmar_ratio": serializers.FloatField(required=False),
                "expected_shortfall": serializers.FloatField(required=False),
                "max_drawdown": serializers.FloatField(required=False),
                "profit_factor": serializers.FloatField(required=False),
                "recovery_factor": serializers.FloatField(required=False),
                "sharpe_ratio": serializers.FloatField(required=False),
                "sortino_ratio": serializers.FloatField(required=False),
                "ulcer_index": serializers.FloatField(required=False),
                "created_at": serializers.IntegerField(required=False),
            },
        ),
        "responses": {
            201: inline_serializer(
                name="SnapshotResponse",
                fields={
                    "success": serializers.BooleanField(),
                    "message": serializers.CharField(),
                    "data": inline_serializer(
                        name="SnapshotData",
                        fields={
                            "_id": serializers.CharField(),
                        },
                    ),
                },
            ),
        },
    }
