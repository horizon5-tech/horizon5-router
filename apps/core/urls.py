from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.core.controllers.backtest import BacktestController
from apps.core.controllers.orders import OrderController
from apps.core.controllers.report import ReportController
from apps.core.controllers.report_performances import ReportPerformancesController
from apps.core.controllers.report_returns import ReportReturnsController
from apps.core.controllers.snapshot import SnapshotController

router = DefaultRouter()

urlpatterns = [
    path(
        "backtests/",
        BacktestController.as_view(),
        name="backtest.get",
    ),
    path(
        "orders/",
        OrderController.as_view(),
        name="order.get",
    ),
    path(
        "reports/",
        ReportController.as_view(),
        name="report.get",
    ),
    path(
        "reports/<str:id>/performances/",
        ReportPerformancesController.as_view(),
        name="report_performances.get",
    ),
    path(
        "reports/<str:id>/returns/",
        ReportReturnsController.as_view(),
        name="report_returns.get",
    ),
    path(
        "snapshots/",
        SnapshotController.as_view(),
        name="snapshot.get",
    ),
    *router.urls,
]
