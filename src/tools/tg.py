from typing import List, Optional

from loguru import logger
from telegram import Bot
from telegram.constants import MessageLimit, ParseMode
from telegram.error import TelegramError

from src.core.config import settings
from src.core.exceptions import TelegramPostError

#: Telegram bot token
TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
#: Telegram chat ID
TELEGRAM_CHAT_ID = settings.TELEGRAM_CHAT_ID
#: Telegram admin chat ID
TELEGRAM_ADMIN_CHAT_ID = settings.TELEGRAM_ADMIN_CHAT_ID
#: Telegram reviewer chat IDs
TELEGRAM_REVIEWER_CHAT_IDS = settings.TELEGRAM_REVIEWER_CHAT_IDS

# Initialize the bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def post_summary_to_telegram(summary_html: str) -> int:
    """
    Post an HTML-formatted message to the Telegram channel.

    Args:
        summary_html (str): The summary text in HTML format.

    Returns:
        int: The message ID of the posted message.

    Raises:
        TelegramPostError: If the message fails to send or if no message ID is returned.
    """
    try:
        message = await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=summary_html,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
        )
        if not message or not message.message_id:
            raise TelegramPostError("No message ID returned from Telegram")
        logger.info(f"Message sent successfully to Telegram with ID: {message.message_id}")
        return message.message_id

    except TelegramError as e:
        error_msg = f"Failed to send message to Telegram: {str(e)}"
        raise TelegramPostError(error_msg) from e


def split_long_message(message: str, chunk_size: int = MessageLimit.MAX_TEXT_LENGTH) -> List[str]:
    """
    Split a long message into chunks that fit within Telegram's message size limit.

    Args:
        message (str): The message to split
        chunk_size (int): Maximum size of each chunk (default: Telegram's limit)

    Returns:
        List[str]: List of message chunks
    """
    # If message is short enough, return it as a single chunk
    if len(message) <= chunk_size:
        return [message]

    chunks = []
    while len(message) > chunk_size:
        chunks.append(message[:chunk_size])
        message = message[chunk_size:]
    chunks.append(message)
    return chunks


async def post_to_admin(message: str) -> Optional[int]:
    """
    Post a message to the admin's personal chat. If the message is too long,
    it will be split into multiple messages.

    Args:
        message (str): The message to send

    Returns:
        Optional[int]: The message ID of the last message if successful, None otherwise

    Raises:
        TelegramPostError: If the message fails to send
    """
    try:
        chunks = split_long_message(message)
        if len(chunks) > 1:
            logger.info(f"Message split into {len(chunks)} chunks")

        last_message_id = None
        for i, chunk in enumerate(chunks, 1):
            response = await bot.send_message(
                chat_id=TELEGRAM_ADMIN_CHAT_ID,
                text=chunk,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )

            if not response or not response.message_id:
                logger.error(f"No message ID returned for chunk {i}")
                continue

            last_message_id = response.message_id
            logger.info(
                f"Message chunk {i}/{len(chunks)} sent successfully with ID: {last_message_id}"
            )
        return last_message_id

    except TelegramError as e:
        error_msg = f"Failed to send message to admin: {str(e)}"
        logger.error(error_msg)
        raise TelegramPostError(error_msg) from e
    except Exception as e:
        error_msg = f"Unexpected error while posting to admin: {str(e)}"
        logger.error(error_msg)
        raise TelegramPostError(error_msg) from e


async def post_to_reviewers(message: str) -> List[Optional[int]]:
    """
    Post a message to all configured reviewer chats. If the message is too long,
    it will be split into multiple messages.

    Args:
        message (str): The message to send

    Returns:
        List[Optional[int]]: List of message IDs for each reviewer's last message

    Raises:
        TelegramPostError: If sending to all reviewers fails
    """
    message_ids = []
    chunks = split_long_message(message)

    for reviewer_id in TELEGRAM_REVIEWER_CHAT_IDS:
        try:
            last_message_id = None
            for i, chunk in enumerate(chunks, 1):
                response = await bot.send_message(
                    chat_id=reviewer_id,
                    text=chunk,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=False,
                )

                if not response or not response.message_id:
                    logger.error(f"No message ID returned for chunk {i} to reviewer {reviewer_id}")
                    continue

                last_message_id = response.message_id
                logger.info(
                    f"Message chunk {i}/{len(chunks)} sent successfully to reviewer {reviewer_id} "
                    f"with ID: {last_message_id}"
                )
            message_ids.append(last_message_id)

        except TelegramError as e:
            logger.error(f"Failed to send message to reviewer {reviewer_id}: {str(e)}")
            message_ids.append(None)
            continue

    if not any(message_ids):
        error_msg = "Failed to send message to all reviewers"
        logger.error(error_msg)
        raise TelegramPostError(error_msg)

    return message_ids
