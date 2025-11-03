from typing import Any, Dict

from drf_spectacular.utils import inline_serializer
from rest_framework import serializers


def response_200_schema(
    controller_name: str,
    response: Dict[str, Any],
) -> Dict[int, Any]:
    return {
        200: inline_serializer(
            name=f"{controller_name}Response",
            fields={
                "success": serializers.BooleanField(),
                "message": serializers.CharField(required=False),
                **response,
            },
        )
    }
