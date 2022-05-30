import os
from telegram import Update
from aws_embedded_metrics import MetricsLogger
from telegram.ext import Filters


def create_metrics(update: Update, metrics: MetricsLogger):
    BOT_NAME = os.environ.get('BOT_NAME')
    metrics.put_dimensions({"bot_name": BOT_NAME})
    metrics.put_metric("Call", 1)
    metrics.set_property("is_command", Filters.command(update))
    metrics.set_property("is_group", Filters.chat_type.group(update))
    metrics.set_property("user_id", update.effective_user.id)
    metrics.set_property("user_name", update.effective_user.name)
    metrics.set_property("is_bot", update.effective_user.is_bot)
    metrics.set_property("text", update.effective_message.text)
