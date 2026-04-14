from typing import Any

from telegram import Update
from telegram.ext import CallbackContext as BaseCallbackContext

from app.models.user import get_or_create_user


class CallbackContext(BaseCallbackContext):
    @property
    def metrics(self) -> Any:
        return getattr(self.application, "metrics", None)

    def user_db(self, update: Update):
        user, created = get_or_create_user(
            update.effective_user.id, update.effective_user.to_dict()
        )
        self.set_metrics_property("is_new_user", created)
        return user

    def set_metrics_property(self, key, value):
        if self.metrics:
            self.metrics.set_property(key, value)
