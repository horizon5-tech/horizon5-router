from typing import Any

from drf_spectacular.utils import OpenApiParameter, inline_serializer
from rest_framework import serializers


def delete_schema() -> Any:
    return {
        "tags": ["Snapshot"],
        "summary": "Delete a snapshot",
        "description": (
            "Deletes an existing snapshot record from the database. "
            "This operation cannot be undone."
        ),
        "parameters": [
            OpenApiParameter(
                name="id",
                type=str,
                location=OpenApiParameter.PATH,
                description="Snapshot ID",
                required=True,
            ),
        ],
        "responses": {
            200: inline_serializer(
                name="SnapshotDeleteResponse",
                fields={
                    "success": serializers.BooleanField(),
                    "message": serializers.CharField(),
                },
            ),
            404: inline_serializer(
                name="SnapshotNotFoundResponse",
                fields={
                    "success": serializers.BooleanField(),
                    "message": serializers.CharField(),
                },
            ),
        },
    }
