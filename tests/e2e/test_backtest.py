import unittest
from typing import List

from apps.core.enums.backtest_status import BacktestStatus
from apps.core.enums.http_status import HttpStatus
from tests.e2e.wrappers.test import TestWrapper

backtests: List[str] = []


class TestBacktest(TestWrapper):
    # ───────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────
    def setUp(self) -> None:
        super().setUp()

    # ───────────────────────────────────────────────────────────
    # PUBLIC METHODS
    # ───────────────────────────────────────────────────────────
    def test_01_create_backtest(self) -> None:
        response = self.execute(
            "POST",
            f"{self._base_url}/api/backtest/",
            body={
                "asset": "btcusdt",
                "from_date": 1714732800,
                "to_date": 1714732800,
            },
        )

        self.assertEqual(response.status_code, HttpStatus.OK.value)

        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIn("success", data)
        self.assertTrue(data["success"])

        backtest_id = data["data"]["_id"]
        backtests.append(backtest_id)
        self.log.info(f"Response: {response.json()}")
        self.log.info(f"Backtest ID added: {backtest_id}")

    def test_02_get_all_backtests(self) -> None:
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

    def test_03_update_backtest(self) -> None:
        self.log.info(f"Available backtest IDs: {backtests}")

        backtest_id = backtests[0]
        response = self.execute(
            "PUT",
            f"{self._base_url}/api/backtest/{backtest_id}/",
            body={
                "status": BacktestStatus.COMPLETED.value,
            },
        )

        self.assertEqual(response.status_code, HttpStatus.OK.value)

        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIn("success", data)
        self.assertTrue(data["success"])

        self.log.info(f"Response: {response.json()}")

    def test_04_delete_backtests(self) -> None:
        self.log.info(f"Deleting backtest IDs: {backtests}")

        for backtest_id in backtests:
            response = self.execute(
                "DELETE",
                f"{self._base_url}/api/backtest/{backtest_id}/",
            )

            self.assertEqual(response.status_code, HttpStatus.OK.value)

            data = response.json()
            self.assertIsInstance(data, dict)
            self.assertIn("success", data)
            self.assertTrue(data["success"])
            self.assertIn("message", data)
            self.assertEqual(data["message"], "Backtest deleted successfully")

            self.log.info(f"Deleted backtest {backtest_id}: {response.json()}")

        backtests.clear()
        self.log.info("All backtests deleted and list cleared")


if __name__ == "__main__":
    unittest.main()
