import os
from pathlib import Path

from telegram.ext import Updater, ContextTypes

try:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".envs" / ".local" / ".app")
except ImportError:
    pass

from app.config import configure, configure_handlers
from app.utils.callback_context import CallbackContext
from app.utils.persistence import DynamodbPersistence

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

updater = Updater(
    TELEGRAM_TOKEN,
    context_types=ContextTypes(context=CallbackContext),
    persistence=DynamodbPersistence()
)
dp = updater.dispatcher
configure_handlers(dp)
configure(dp.bot)
updater.start_polling()
updater.idle()
