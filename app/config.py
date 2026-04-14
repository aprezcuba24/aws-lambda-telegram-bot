from telegram import Bot, BotCommandScopeAllGroupChats
from telegram.ext import Application, CallbackQueryHandler, CommandHandler

from app.handlers.start import start_command, start_query


async def configure(bot: Bot):
    common_commands = []
    await bot.set_my_commands(commands=common_commands, scope=BotCommandScopeAllGroupChats())
    await bot.set_my_commands([("start", "Start to use the bot.")] + common_commands)


def configure_handlers(application: Application) -> None:
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(start_query, pattern="start"))
