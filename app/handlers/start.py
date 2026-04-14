from string import Template
from telegram import Update

from app.utils.callback_context import CallbackContext


START_TEXT = """
Hello "$name"!!
"""


def _content(user_model):
    return dict(text=Template(START_TEXT).substitute(name=user_model["complete_name"]))


async def start_query(update: Update, context: CallbackContext):
    await update.effective_message.edit_text(**_content(context.user_db(update)))


async def start_command(update: Update, context: CallbackContext):
    await update.effective_message.reply_text(**_content(context.user_db(update)))
