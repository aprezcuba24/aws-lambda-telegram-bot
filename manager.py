import os
from telegram.ext import Updater, ContextTypes

from app.config import configure, configure_handlers
from app.utils.callback_context import CallbackContext

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

updater = Updater(TELEGRAM_TOKEN, context_types=ContextTypes(context=CallbackContext))
dp = updater.dispatcher
configure_handlers(dp)
configure(dp.bot)
updater.start_polling()
updater.idle()
