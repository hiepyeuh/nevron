# from unittest.mock import AsyncMock, MagicMock, patch
# import pytest
# from loguru import logger
# from telegram import Bot, Message
# from telegram.constants import MessageLimit
# from telegram.error import TelegramError as TGError

# from src.core.config import settings
# from src.core.exceptions import TelegramError
# from src.tools.tg import split_long_message, post_summary_to_telegram


# @pytest.fixture
# def mock_tool_logger(monkeypatch):
#     """Mock logger for tool testing."""
#     mock_debug = MagicMock()
#     mock_error = MagicMock()
#     monkeypatch.setattr(logger, "debug", mock_debug)
#     monkeypatch.setattr(logger, "error", mock_error)
#     return mock_debug, mock_error


# @pytest.fixture
# def mock_telegram_settings(monkeypatch):
#     """Mock Telegram settings."""
#     monkeypatch.setattr(settings, "TELEGRAM_CHAT_ID", "test_chat_id")
#     return settings


# @pytest.fixture
# def mock_telegram_bot():
#     """Create a mock Telegram bot."""
#     mock_bot = AsyncMock(spec=Bot)
#     return mock_bot


# def test_split_long_message_short():
#     """Test splitting a message that's already within limits."""
#     # arrange:
#     message = "Short message"

#     # act:
#     chunks = split_long_message(message)

#     # assert:
#     assert len(chunks) == 1
#     assert chunks[0] == message


# def test_split_long_message_exact():
#     """Test splitting a message that's exactly at the limit."""
#     # arrange:
#     chunk_size = 10
#     message = "A" * chunk_size

#     # act:
#     chunks = split_long_message(message, chunk_size)

#     # assert:
#     assert len(chunks) == 1
#     assert chunks[0] == message


# def test_split_long_message_multiple_chunks():
#     """Test splitting a long message into multiple chunks."""
#     # arrange:
#     chunk_size = 10
#     message = "A" * 25  # Will create 3 chunks

#     # act:
#     chunks = split_long_message(message, chunk_size)

#     # assert:
#     assert len(chunks) == 3
#     assert all(len(chunk) <= chunk_size for chunk in chunks)
#     assert "".join(chunks) == message


# def test_split_long_message_telegram_limit():
#     """Test splitting using Telegram's actual message limit."""
#     # arrange:
#     message = "A" * (MessageLimit.MAX_TEXT_LENGTH + 100)

#     # act:
#     chunks = split_long_message(message)

#     # assert:
#     assert len(chunks) == 2
#     assert all(len(chunk) <= MessageLimit.MAX_TEXT_LENGTH for chunk in chunks)
#     assert "".join(chunks) == message


# @pytest.mark.asyncio
# async def test_post_summary_to_telegram_success(
#     mock_tool_logger, mock_telegram_settings, mock_telegram_bot
# ):
#     """Test successful posting of a message to Telegram."""
#     # arrange:
#     mock_debug, mock_error = mock_tool_logger
#     summary = "Test message"
#     mock_message = MagicMock(spec=Message)
#     mock_message.message_id = 12345
#     mock_telegram_bot.send_message.return_value = mock_message

#     # act:
#     message_ids = await post_summary_to_telegram(summary, bot=mock_telegram_bot)

#     # assert:
#     assert message_ids == [12345]
#     mock_telegram_bot.send_message.assert_called_once_with(
#         chat_id=mock_telegram_settings.TELEGRAM_CHAT_ID,
#         text=summary,
#         parse_mode="HTML",
#         disable_web_page_preview=False,
#     )
#     mock_debug.assert_called_once()
#     mock_error.assert_not_called()


# @pytest.mark.asyncio
# async def test_post_summary_to_telegram_long_message(
#     mock_tool_logger, mock_telegram_settings, mock_telegram_bot
# ):
#     """Test posting a long message that needs to be split."""
#     # arrange:
#     mock_debug, mock_error = mock_tool_logger
#     summary = "A" * (MessageLimit.MAX_TEXT_LENGTH + 100)
#     mock_message1 = MagicMock(spec=Message, message_id=12345)
#     mock_message2 = MagicMock(spec=Message, message_id=12346)
#     mock_telegram_bot.send_message.side_effect = [mock_message1, mock_message2]

#     # act:
#     message_ids = await post_summary_to_telegram(summary, bot=mock_telegram_bot)

#     # assert:
#     assert message_ids == [12345, 12346]
#     assert mock_telegram_bot.send_message.call_count == 2
#     assert mock_debug.call_count == 2
#     mock_error.assert_not_called()


# @pytest.mark.asyncio
# async def test_post_summary_to_telegram_no_message_id(
#     mock_tool_logger, mock_telegram_settings, mock_telegram_bot
# ):
#     """Test error handling when Telegram doesn't return a message ID."""
#     # arrange:
#     mock_debug, mock_error = mock_tool_logger
#     summary = "Test message"
#     mock_message = MagicMock(spec=Message)
#     mock_message.message_id = None
#     mock_telegram_bot.send_message.return_value = mock_message

#     # act/assert:
#     with pytest.raises(TelegramError, match="No message ID returned from Telegram"):
#         await post_summary_to_telegram(summary, bot=mock_telegram_bot)


# @pytest.mark.asyncio
# async def test_post_summary_to_telegram_api_error(
#     mock_tool_logger, mock_telegram_settings, mock_telegram_bot
# ):
#     """Test error handling when Telegram API returns an error."""
#     # arrange:
#     mock_debug, mock_error = mock_tool_logger
#     summary = "Test message"
#     mock_telegram_bot.send_message.side_effect = TGError("API Error")

#     # act/assert:
#     with pytest.raises(TelegramError, match="Failed to send message to Telegram"):
#         await post_summary_to_telegram(summary, bot=mock_telegram_bot)
