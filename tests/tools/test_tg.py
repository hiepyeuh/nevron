# import pytest
# from unittest.mock import AsyncMock, MagicMock, patch

# from telegram import Bot, Message
# from telegram.constants import MessageLimit, ParseMode
# from telegram.error import TelegramError

# from src.tools.tg import split_long_message, post_summary_to_telegram
# from src.core.exceptions import TelegramError as TelegramPostError


# TELEGRAM_CHAT_ID = "1234567890"

# @pytest.fixture
# def mock_bot():
#     """Mock the Telegram Bot instance."""
#     return AsyncMock(spec=Bot)


# @pytest.mark.parametrize(
#     "message,chunk_size,expected",
#     [
#         ("Short message", MessageLimit.MAX_TEXT_LENGTH, ["Short message"]),
#         (
#             "A" * (MessageLimit.MAX_TEXT_LENGTH + 10),
#             MessageLimit.MAX_TEXT_LENGTH,
#             ["A" * MessageLimit.MAX_TEXT_LENGTH, "A" * 10],
#         ),
#         ("", MessageLimit.MAX_TEXT_LENGTH, [""]),
#     ],
# )
# def test_split_long_message(message, chunk_size, expected):
#     """Test splitting long messages into chunks."""
#     result = split_long_message(message, chunk_size=chunk_size)
#     assert result == expected


# @pytest.mark.asyncio
# async def test_post_summary_to_telegram_success(mock_bot):
#     """Test successfully posting a message to Telegram."""
#     # Arrange
#     summary_html = "<b>Test message</b>"
#     mock_message = MagicMock(spec=Message)
#     mock_message.message_id = 12345
#     mock_bot.send_message.return_value = mock_message

#     # Act
#     with patch("src.tools.tg.bot", mock_bot):
#         result = await post_summary_to_telegram(summary_html)

#     # Assert
#     assert result == [12345]
#     mock_bot.send_message.assert_called_once_with(
#         chat_id=TELEGRAM_CHAT_ID,
#         text=summary_html,
#         parse_mode=ParseMode.HTML,
#         disable_web_page_preview=False,
#     )


# @pytest.mark.asyncio
# async def test_post_summary_to_telegram_long_message(mock_bot):
#     """Test posting a long message split into multiple chunks."""
#     # Arrange
#     summary_html = "<b>" + "A" * (MessageLimit.MAX_TEXT_LENGTH + 50) + "</b>"
#     message_chunks = split_long_message(summary_html)
#     mock_messages = [MagicMock(spec=Message, message_id=i) for i in range(len(message_chunks))]
#     mock_bot.send_message.side_effect = mock_messages

#     # Act
#     with patch("src.tools.tg.bot", mock_bot):
#         result = await post_summary_to_telegram(summary_html)

#     # Assert
#     assert result == [message.message_id for message in mock_messages]
#     assert mock_bot.send_message.call_count == len(message_chunks)


# @pytest.mark.asyncio
# async def test_post_summary_to_telegram_no_message_id(mock_bot):
#     """Test handling when no message ID is returned."""
#     # Arrange
#     summary_html = "<b>Test message</b>"
#     mock_bot.send_message.return_value = None

#     # Act & Assert
#     with patch("src.tools.tg.bot", mock_bot):
#         with pytest.raises(TelegramPostError, match="No message ID returned from Telegram"):
#             await post_summary_to_telegram(summary_html)


# @pytest.mark.asyncio
# async def test_post_summary_to_telegram_telegram_error(mock_bot):
#     """Test handling a TelegramError during message posting."""
#     # Arrange
#     summary_html = "<b>Test message</b>"
#     mock_bot.send_message.side_effect = TelegramError("Mock Telegram error")

#     # Act & Assert
#     with patch("src.tools.tg.bot", mock_bot):
#         with pytest.raises(TelegramPostError, match="Failed to send message to Telegram"):
#             await post_summary_to_telegram(summary_html)
