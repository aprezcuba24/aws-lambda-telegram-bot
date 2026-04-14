import asyncio
import json
import os

from telegram import Bot, Update
from telegram.ext import Application, ContextTypes

from app.config import configure
from app.utils.callback_context import CallbackContext
from app.utils.dispatcher import MetricsApplication
from app.utils.persistence import DynamodbPersistence


def main(event, context):
    print(event)
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
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


async def _webhook_async(bot: Bot, update_payload: dict) -> None:
    application = (
        Application.builder()
        .application_class(MetricsApplication)
        .bot(bot)
        .persistence(DynamodbPersistence())
        .context_types(ContextTypes(context=CallbackContext))
        .build()
    )
    await application.initialize()
    update = Update.de_json(update_payload, bot)
    await application.process_update(update)
    await application.shutdown()


def webhook(event, bot: Bot):
    data = json.loads(event["body"])
    asyncio.run(_webhook_async(bot, data))
    return {
        "statusCode": 200,
        "body": "ok",
    }


def register_bot(event, bot: Bot):
    url = f"https://{event['requestContext']['domainName']}/webhook"
    bot.set_webhook(url=url)
    body = {
        "webhook_url": url,
        "bot": bot.get_me().to_dict(),
        "input": event,
    }
    configure(bot)
    return {
        "statusCode": 200,
        "body": json.dumps(body),
    }
