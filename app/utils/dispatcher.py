from telegram.ext import Dispatcher as BaseDispatcher
from aws_embedded_metrics import metric_scope, MetricsLogger

from app.utils.metrics import create_metrics


class Dispatcher(BaseDispatcher):
    metrics: MetricsLogger

    @metric_scope
    def process_update(self, update: object, metrics: MetricsLogger) -> None:
        self.metrics = metrics
        create_metrics(update, metrics)
        super().process_update(update)
