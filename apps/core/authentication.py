from typing import Any, Dict, Optional, Tuple

from django.conf import settings
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request


class APIKeyAuthentication(BaseAuthentication):
    keyword = "X-API-Key"

    def authenticate(self, request: Request) -> Optional[Tuple[None, None]]:
        api_key = request.headers.get(self.keyword)
        expected_key = getattr(settings, "API_KEY", None)

        if not api_key:
            raise AuthenticationFailed("API Key is required")

        if not expected_key:
            raise AuthenticationFailed("API Key not configured")

        if api_key != expected_key:
            raise AuthenticationFailed("Invalid API Key")

        return (None, None)


class APIKeyAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "apps.core.authentication.APIKeyAuthentication"
    name = "ApiKeyAuth"

    def get_security_definition(self, auto_schema: Any) -> Dict[str, str]:
        return {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
        }
