import telegram
from telegram.ext import CommandHandler, CallbackQueryHandler

from app.handlers.start import start_command, start_query

def configure(bot: telegram.Bot):
    common_commands = []
    bot.set_my_commands(
        commands=common_commands, scope=telegram.BotCommandScopeAllGroupChats()
    )
    bot.set_my_commands([
        ("start", "Start to use the bot."),
    ] + common_commands)

def configure_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler(command="start", callback=start_command))
    dispatcher.add_handler(CallbackQueryHandler(start_query, pattern="start"))
