import unittest
from datetime import UTC, datetime
from typing import List

from apps.core.enums.http_status import HttpStatus
from tests.e2e.wrappers.test import TestWrapper

snapshots: List[str] = []
backtests: List[str] = []


class TestSnapshot(TestWrapper):
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
                "strategies": "ema5_breakout",
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
        self.log.info(f"Backtest ID added: {backtest_id}")

    def test_02_create_snapshot(self) -> None:
        created_at = datetime.now(UTC)

        response = self.execute(
            "POST",
            f"{self._base_url}/api/snapshot/",
            body={
                "backtest": True,
                "backtest_id": backtests[0],
                "strategy_id": "ema5_breakout",
                "event": "on_trade",
                "nav": 10500.50,
                "allocation": 0.85,
                "nav_peak": 11000.00,
                "r2": 0.92,
                "cagr": 0.35,
                "calmar_ratio": 2.5,
                "expected_shortfall": -0.05,
                "max_drawdown": -0.15,
                "profit_factor": 1.8,
                "recovery_factor": 3.2,
                "sharpe_ratio": 1.5,
                "sortino_ratio": 2.1,
                "ulcer_index": 0.08,
                "created_at": int(created_at.timestamp()),
            },
        )

        self.assertEqual(response.status_code, HttpStatus.OK.value)

        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIn("success", data)
        self.assertTrue(data["success"])

        snapshot_id = data["data"]["_id"]
        snapshots.append(snapshot_id)
        self.log.info(f"Snapshot ID added: {snapshot_id}")

    def test_03_get_all_snapshots(self) -> None:
        response = self.execute(
            "GET",
            f"{self._base_url}/api/snapshots/",
            query=None,
            body=None,
            headers=None,
        )

        self.assertEqual(response.status_code, HttpStatus.OK.value)

        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIn("success", data)
        self.assertTrue(data["success"])

    def test_04_delete_snapshots(self) -> None:
        self.log.info(f"Deleting snapshot IDs: {snapshots}")

        for snapshot_id in snapshots:
            response = self.execute(
                "DELETE",
                f"{self._base_url}/api/snapshot/{snapshot_id}/",
            )

            self.assertEqual(response.status_code, HttpStatus.OK.value)

            data = response.json()
            self.assertIsInstance(data, dict)
            self.assertIn("success", data)
            self.assertTrue(data["success"])
            self.assertIn("message", data)
            self.assertEqual(data["message"], "Snapshot deleted successfully")

            self.log.info(f"Deleted snapshot {snapshot_id}: {response.json()}")

        snapshots.clear()
        self.log.info("All snapshots deleted and list cleared")

    def test_05_delete_backtests(self) -> None:
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
