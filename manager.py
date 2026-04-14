import os
from pathlib import Path
import asyncio

from telegram.ext import Application, ContextTypes

try:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".envs" / ".local" / ".app")
except ImportError:
    pass

from app.config import configure, configure_handlers
from app.utils.callback_context import CallbackContext
from app.utils.dispatcher import MetricsApplication
from app.utils.persistence import DynamodbPersistence

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

application = (
    Application.builder()
    .application_class(MetricsApplication)
    .token(TELEGRAM_TOKEN)
    .persistence(DynamodbPersistence())
    .context_types(ContextTypes(context=CallbackContext))
    .build()
)
loop = asyncio.get_event_loop()
loop.create_task(configure(application.bot))

configure_handlers(application)
print("Service is started")
application.run_polling()
