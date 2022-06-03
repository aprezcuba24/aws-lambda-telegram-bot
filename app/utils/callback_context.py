from telegram import Update
from telegram.ext import CallbackContext as BaseCallbackContext, Dispatcher

from app.models.user import get_or_create_user
from aws_embedded_metrics import MetricsLogger


class CallbackContext(BaseCallbackContext):
    _update: Update
    metrics: MetricsLogger

    @classmethod
    def from_update(cls, update: Update, dispatcher: Dispatcher) -> "CallbackContext":
        context = super().from_update(update, dispatcher)
        context._update = update
        context.metrics = getattr(dispatcher, "metrics", None)
        return context

    @property
    def user_db(self):
        user, created = get_or_create_user(
            self._update.effective_user.id, self._update.effective_user.to_dict()
        )
        self.set_metrics_property("is_new_user", created)
        return user

    def set_metrics_property(self, key, value):
        if self.metrics:
            self.metrics.set_property(key, value)
