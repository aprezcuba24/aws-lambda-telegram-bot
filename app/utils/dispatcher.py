from typing import Any

from telegram.ext import Application

from app.utils.dynamodb import is_local_dynamo_dev
from app.utils.metrics import NoopMetricsLogger, create_metrics

try:
    from aws_embedded_metrics import MetricsLogger, metric_scope

    _HAS_EMBEDDED_METRICS = True
except ImportError:
    MetricsLogger = object  # type: ignore[misc,assignment]
    metric_scope = None  # type: ignore[assignment]
    _HAS_EMBEDDED_METRICS = False


class MetricsApplication(Application):
    metrics: Any

    async def process_update(self, update: object) -> None:
        if not _HAS_EMBEDDED_METRICS or is_local_dynamo_dev():
            self.metrics = NoopMetricsLogger()
            create_metrics(update, self.metrics)
            return await super().process_update(update)
        return await self._process_update_with_metrics(update)


async def _process_update_with_metrics_impl(self: MetricsApplication, update: object, metrics: MetricsLogger) -> None:
    self.metrics = metrics
    create_metrics(update, metrics)
    await super(MetricsApplication, self).process_update(update)


if _HAS_EMBEDDED_METRICS and metric_scope is not None:
    MetricsApplication._process_update_with_metrics = metric_scope(_process_update_with_metrics_impl)  # type: ignore[method-assign]
else:

    async def _process_update_with_metrics_fallback(self: MetricsApplication, update: object) -> None:
        self.metrics = NoopMetricsLogger()
        create_metrics(update, self.metrics)
        await super(MetricsApplication, self).process_update(update)

    MetricsApplication._process_update_with_metrics = _process_update_with_metrics_fallback  # type: ignore[method-assign]
