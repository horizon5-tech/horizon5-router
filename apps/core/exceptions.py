from typing import Any, Optional

from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.views import exception_handler

from apps.core.enums.http_status import HttpStatus


def custom_exception_handler(exc: Exception, context: Any) -> Optional[JsonResponse]:
    response = exception_handler(exc, context)

    if response is not None:
        custom_response = {
            "success": False,
            "message": None,
        }

        if isinstance(exc, AuthenticationFailed):
            custom_response["message"] = str(exc)
            return JsonResponse(
                custom_response,
                status=HttpStatus.FORBIDDEN.value,
            )

        if isinstance(exc, ValidationError):
            custom_response["message"] = response.data
            return JsonResponse(
                custom_response,
                status=response.status_code,
            )

        custom_response["message"] = str(exc)
        return JsonResponse(
            custom_response,
            status=response.status_code,
        )

    return response
