import os
from telegram.ext import Updater, ContextTypes

from app.register_webhook import configure
from app.utils.callback_context import CallbackContext
from app.webhook import configure as configure_handlers

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

updater = Updater(TELEGRAM_TOKEN, context_types=ContextTypes(context=CallbackContext))
dp = updater.dispatcher
configure_handlers(dp)
configure(dp.bot)
updater.start_polling()
updater.idle()
