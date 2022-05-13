import json
import os
from telegram import Update, Bot
from telegram.ext import ContextTypes
from queue import Queue
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler

from app.handlers.start import start_command, start_query
from app.utils.callback_context import CallbackContext


def main(event, context):
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    bot = Bot(token=TELEGRAM_TOKEN)
    print(event)
    data = json.loads(event["body"])
    update = Update.de_json(data, bot)
    dispatcher = Dispatcher(bot=bot, update_queue=Queue(), context_types=ContextTypes(context=CallbackContext))
    configure(dispatcher)
    dispatcher.process_update(update=update)
    return {
        "statusCode": 200,
        "body": "ok"
    }

def configure(dispatcher):
    dispatcher.add_handler(CommandHandler(command="start", callback=start_command))
    dispatcher.add_handler(CallbackQueryHandler(start_query, pattern="start"))
