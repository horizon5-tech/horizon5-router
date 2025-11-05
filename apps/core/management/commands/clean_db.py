import logging
from typing import Any

from django.core.management.base import BaseCommand

from apps.core.models.backtest import BacktestModel


class Command(BaseCommand):
    help = "Truncate all collections in MongoDB by deleting all documents"

    def handle(self, *_args: Any, **_options: Any) -> None:
        log = logging.getLogger(__name__)

        model = BacktestModel()
        backtests = model.find(query_filters={})

        for backtest in backtests:
            try:
                model.delete(query_filters={"_id": backtest["_id"]})
                log.info(f"Deleted backtest: {backtest['_id']}")

            except Exception as e:
                log.error(f"Error deleting backtest: {backtest['_id']}: {e!r}")
