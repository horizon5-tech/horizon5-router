from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.core.controllers.backtest import BacktestController

router = DefaultRouter()

urlpatterns = [
    path("backtests/", BacktestController.as_view(), name="backtest.get"),
    *router.urls,
]
