from typing import Any

from drf_spectacular.utils import inline_serializer
from rest_framework import serializers

from apps.core.schemas.pagination import pagination_schema
from apps.core.schemas.responses import response_200_schema


def get_schema() -> Any:
    return {
        "tags": ["Snapshot"],
        "summary": "Get snapshots",
        "description": (
            "Provides a list of snapshots saved on the database, "
            "and also allows to filter the results by various parameters."
        ),
        "parameters": [
            *pagination_schema(),
        ],
        "responses": {
            **response_200_schema(
                "SnapshotController",
                {
                    "data": inline_serializer(
                        name="Snapshots",
                        fields={
                            "id": serializers.CharField(),
                            "created_at": serializers.DateTimeField(),
                            "updated_at": serializers.DateTimeField(),
                        },
                    ),
                },
            ),
        },
    }
