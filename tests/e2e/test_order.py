import unittest
from datetime import UTC, datetime
from typing import List

from apps.core.enums.http_status import HttpStatus
from tests.e2e.wrappers.test import TestWrapper

orders: List[str] = []


class TestOrder(TestWrapper):
    # ───────────────────────────────────────────────────────────
    # CONSTRUCTOR
    # ───────────────────────────────────────────────────────────
    def setUp(self) -> None:
        super().setUp()

    # ───────────────────────────────────────────────────────────
    # PUBLIC METHODS
    # ───────────────────────────────────────────────────────────
    def test_01_create_order(self) -> None:
        created_at = datetime.now(UTC)
        updated_at = datetime.now(UTC)

        response = self.execute(
            "POST",
            f"{self._base_url}/api/order/",
            body={
                "backtest": True,
                "backtest_id": "690a08adc741ec5f14b8e628",
                "strategy_id": "ema5_breakout",
                "symbol": "BTCUSDT",
                "gateway": "binance",
                "side": "buy",
                "order_type": "market",
                "status": "closed",
                "volume": 0.07493382240856099,
                "executed_volume": 0.07493382240856099,
                "price": 110260.78,
                "close_price": 111386.07,
                "take_profit_price": 111363.3878,
                "stop_loss_price": 99234.70199999999,
                "client_order_id": "hrz-f4746dc603a0",
                "filled": True,
                "profit": 84.3222810181302,
                "profit_percentage": 0.01020571412609278,
                "created_at": int(created_at.timestamp()),
                "updated_at": int(updated_at.timestamp()),
            },
        )

        self.assertEqual(response.status_code, HttpStatus.CREATED.value)

        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIn("success", data)
        self.assertTrue(data["success"])

        order_id = data["data"]["_id"]
        orders.append(order_id)
        self.log.info(f"Order ID added: {order_id}")

    def test_02_get_all_orders(self) -> None:
        response = self.execute(
            "GET",
            f"{self._base_url}/api/orders/",
            query=None,
            body=None,
            headers=None,
        )

        self.assertEqual(response.status_code, HttpStatus.OK.value)

        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIn("success", data)
        self.assertTrue(data["success"])

    def test_03_update_order(self) -> None:
        self.log.info(f"Available order IDs: {orders}")

        order_id = orders[0]
        updated_at = datetime.now(UTC)

        response = self.execute(
            "PUT",
            f"{self._base_url}/api/order/{order_id}/",
            body={
                "strategy_id": "updated_source",
                "symbol": "ETHUSDT",
                "status": "filled",
                "volume": 0.1,
                "filled": True,
                "close_price": 111500.50,
                "profit": 100.50,
                "profit_percentage": 0.012,
                "updated_at": int(updated_at.timestamp()),
            },
        )

        self.assertEqual(response.status_code, HttpStatus.OK.value)

        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertIn("success", data)
        self.assertTrue(data["success"])

    def test_04_delete_orders(self) -> None:
        self.log.info(f"Deleting order IDs: {orders}")

        for order_id in orders:
            response = self.execute(
                "DELETE",
                f"{self._base_url}/api/order/{order_id}/",
            )

            self.assertEqual(response.status_code, HttpStatus.OK.value)

            data = response.json()
            self.assertIsInstance(data, dict)
            self.assertIn("success", data)
            self.assertTrue(data["success"])
            self.assertIn("message", data)
            self.assertEqual(data["message"], "Order deleted successfully")

            self.log.info(f"Deleted order {order_id}: {response.json()}")

        orders.clear()
        self.log.info("All orders deleted and list cleared")


if __name__ == "__main__":
    unittest.main()
