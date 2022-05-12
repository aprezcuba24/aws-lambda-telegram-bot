import json
import os
import telegram


def configure(bot: telegram.Bot):
    common_commands = []
    bot.set_my_commands(
        commands=common_commands, scope=telegram.BotCommandScopeAllGroupChats()
    )
    bot.set_my_commands([
        ("start", "Start to use the bot."),
    ] + common_commands)


def main(event, context):
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    url = f"https://{event['requestContext']['domainName']}/webhook"
    bot.setWebhook(url)
    body = {
        "webhook_url": url,
        "bot": bot.get_me().to_dict(),
        "input": event
    }
    configure(bot)

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
