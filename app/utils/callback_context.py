from telegram import Update
from telegram.ext import CallbackContext as BaseCallbackContext, Dispatcher

from app.models.user import get_or_create_user


class CallbackContext(BaseCallbackContext):
    _update: Update

    @classmethod
    def from_update(cls, update: Update, dispatcher: Dispatcher) -> "CallbackContext":
        context = super().from_update(update, dispatcher)
        context._update = update
        return context

    @property
    def user_db(self):
        return get_or_create_user(
            self._update.effective_user.id, self._update.effective_user.to_dict()
        )
