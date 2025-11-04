import unittest

from apps.core.enums.http_status import HttpStatus
from tests.e2e.wrappers.test import TestWrapper


class TestBacktest(TestWrapper):
    def test_get_all_backtests(self) -> None:
        response = self.execute(
            "GET",
            f"{self._base_url}/api/backtests/",
            query=None,
            body=None,
            headers=None,
        )

        self.assertEqual(response.status_code, HttpStatus.OK.value)

        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIn("success", data)
        self.assertTrue(data["success"])

        self.log.info(f"Response: {response.json()}")


if __name__ == "__main__":
    unittest.main()
