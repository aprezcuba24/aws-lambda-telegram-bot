from unittest.mock import AsyncMock, Mock

import pytest
from telegram import Update

from app.handlers.start import start_command
from app.utils.callback_context import CallbackContext


@pytest.mark.asyncio
async def test_start_command():
    update = AsyncMock(spec=Update)
    update.effective_message.reply_text = AsyncMock()
    context = AsyncMock(spec=CallbackContext)
    context.user_db = Mock(return_value={"complete_name": "Test"})
    await start_command(update, context)
    assert update.effective_message.reply_text.called
    update.effective_message.reply_text.assert_called_once_with(text='\nHello "Test"!!\n')
