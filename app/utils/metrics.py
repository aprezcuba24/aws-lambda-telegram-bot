import os
from telegram import Update
from aws_embedded_metrics import MetricsLogger
from telegram.ext import Filters


def create_metrics(update: Update, metrics: MetricsLogger):
    BOT_NAME = os.environ.get('BOT_NAME')
    metrics.put_dimensions({"bot_name": BOT_NAME})
    metrics.put_metric("Call", 1)
    if update.inline_query:
        metrics.set_property("is_inline_query", 1)
        metrics.set_property("inline_query", update.inline_query.query)
    else:
        metrics.set_property("is_command", Filters.command(update))
        metrics.set_property("is_private", Filters.chat_type.private(update))
        metrics.set_property("text", update.effective_message.text)
    metrics.set_property("user_id", update.effective_user.id)
    metrics.set_property("user_name", update.effective_user.name)
    metrics.set_property("is_bot", update.effective_user.is_bot)
