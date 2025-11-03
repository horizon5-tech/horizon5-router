from typing import List

from drf_spectacular.utils import OpenApiParameter


def pagination_schema() -> List[OpenApiParameter]:
    return [
        OpenApiParameter(
            name="page",
            type=int,
            location=OpenApiParameter.QUERY,
            description="Page number",
            default=1,
        ),
        OpenApiParameter(
            name="page_size",
            type=int,
            location=OpenApiParameter.QUERY,
            description="Number of items per page",
            default=10,
        ),
        OpenApiParameter(
            name="sort",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Field to sort by",
            default="created_at",
        ),
        OpenApiParameter(
            name="sort_order",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Sort order (asc or desc)",
            default="desc",
            enum=["asc", "desc"],
        ),
    ]
