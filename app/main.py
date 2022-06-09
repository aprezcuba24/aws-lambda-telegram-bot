import json
import os
from telegram import Update, Bot
from telegram.ext import ContextTypes
from queue import Queue

from app.utils.callback_context import CallbackContext
from app.config import configure, configure_handlers
from app.utils.dispatcher import Dispatcher
from app.utils.persistence import DynamodbPersistence


def main(event, context):
    print(event)
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    bot = Bot(token=TELEGRAM_TOKEN)
    routes = {
        "/webhook": webhook,
        "/register-bot": register_bot,
    }
    func = routes.get(event["rawPath"], not_found)
    return func(event, bot)


def not_found(event, *args):
    return {
        "statusCode": 404,
        "body": "Not found",
    }


def webhook(event, bot: Bot):
    data = json.loads(event["body"])
    update = Update.de_json(data, bot)
    dispatcher = Dispatcher(
        bot=bot,
        update_queue=Queue(),
        context_types=ContextTypes(context=CallbackContext),
        persistence=DynamodbPersistence()
    )
    configure_handlers(dispatcher)
    dispatcher.process_update(update=update)
    return {
        "statusCode": 200,
        "body": "ok"
    }


def register_bot(event, bot: Bot):
    url = f"https://{event['requestContext']['domainName']}/webhook"
    bot.setWebhook(url)
    body = {
        "webhook_url": url,
        "bot": bot.get_me().to_dict(),
        "input": event
    }
    configure(bot)
    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }
