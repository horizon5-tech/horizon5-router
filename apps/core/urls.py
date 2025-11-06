from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.core.controllers.backtest import BacktestController
from apps.core.controllers.orders import OrderController
from apps.core.controllers.report import ReportController
from apps.core.controllers.snapshot import SnapshotController

router = DefaultRouter()

urlpatterns = [
    path(
        "backtests/",
        BacktestController.as_view(http_method_names=["get"]),
        name="backtest.get",
    ),
    path(
        "backtest/",
        BacktestController.as_view(http_method_names=["post"]),
        name="backtest.post",
    ),
    path(
        "backtest/<str:id>/",
        BacktestController.as_view(http_method_names=["put", "patch", "delete"]),
        name="backtest.update",
    ),
    path(
        "orders/",
        OrderController.as_view(http_method_names=["get"]),
        name="order.get",
    ),
    path(
        "order/",
        OrderController.as_view(http_method_names=["post"]),
        name="order.post",
    ),
    path(
        "order/<str:id>/",
        OrderController.as_view(http_method_names=["put", "patch", "delete"]),
        name="order.update",
    ),
    path(
        "reports/",
        ReportController.as_view(),
        name="report.get",
    ),
    path(
        "snapshots/",
        SnapshotController.as_view(http_method_names=["get"]),
        name="snapshot.get",
    ),
    path(
        "snapshot/",
        SnapshotController.as_view(http_method_names=["post"]),
        name="snapshot.post",
    ),
    path(
        "snapshot/<str:id>/",
        SnapshotController.as_view(http_method_names=["put", "patch", "delete"]),
        name="snapshot.update",
    ),
    *router.urls,
]
