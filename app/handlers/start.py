from telegram import Update
from telegram.ext import CallbackContext


START_TEXT = '''
Some text here
'''

def _content():
    return dict(text=START_TEXT)

def start_query(update: Update, context: CallbackContext):
    update.effective_message.edit_text(**_content())

def start_command(update: Update, context: CallbackContext):
    update.effective_message.reply_text(**_content())
