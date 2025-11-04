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
                "session_id": serializers.IntegerField(),
                "event": serializers.CharField(),
                "date": serializers.IntegerField(),
                "nav": serializers.FloatField(),
                "allocation": serializers.FloatField(),
                "nav_peak": serializers.FloatField(),
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
