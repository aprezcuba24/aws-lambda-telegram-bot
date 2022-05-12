import os
from telegram.ext import Updater

from app.register_webhook import configure
from app.webhook import configure as configure_handlers

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

updater = Updater(TELEGRAM_TOKEN)
dp = updater.dispatcher
configure_handlers(dp)
configure(dp.bot)
updater.start_polling()
updater.idle()
