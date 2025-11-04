import logging
import unittest
from typing import Any, Dict, Optional

import requests
from django.conf import settings


class TestWrapper(unittest.TestCase):
    # ───────────────────────────────────────────────────────────
    # PROPERTIES
    # ───────────────────────────────────────────────────────────
    log = logging.getLogger(__name__)
    _base_url: str
    _api_key: Optional[str]
    _headers: Dict[str, str]

    # ───────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────
    def __init__(self, methodName: str = "runTest") -> None:  # noqa: N803
        super().__init__(methodName)

        self._base_url = getattr(settings, "BASE_URL", "http://localhost:8000")
        self._api_key = getattr(settings, "API_KEY", None)

        self._prepare_headers()

    def execute(
        self,
        method: str,
        url: str,
        query: Optional[Dict[str, Any]] = {},
        body: Optional[Dict[str, Any]] = {},
        headers: Optional[Dict[str, str]] = {},
    ) -> Any:
        if query is None:
            query = {}

        if body is None:
            body = {}

        if headers is None:
            headers = {}

        self._headers = {
            **self._headers,
            **headers,
        }

        try:
            response = requests.request(
                method,
                url,
                headers=self._headers,
                json=body,
                params=query,
            )
        except requests.exceptions.RequestException as e:
            raise e

        return response

    # ───────────────────────────────────────────────────────────
    # PRIVATE METHODS
    # ───────────────────────────────────────────────────────────
    def _prepare_headers(self) -> None:
        if self._api_key is None:
            raise ValueError("API_KEY is not configured in Django settings")

        self._headers = {
            "X-API-Key": self._api_key,
            "Content-Type": "application/json",
        }
