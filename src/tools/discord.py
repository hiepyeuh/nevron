from typing import Callable, Optional

import aiohttp
import discord
from discord.ext import commands
from loguru import logger

from src.core.config import settings
from src.core.exceptions import DiscordError


class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        # Disable SSL for development
        connector = aiohttp.TCPConnector(verify_ssl=False)
        # Initialize super class with TCP connector
        super().__init__(command_prefix="!", intents=intents, connector=connector)
        # Set the SSL context for HTTP client
        self.http.connector = connector

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        """
        Start the Discord bot.

        Args:
            token (str): Discord bot token for authentication
            reconnect (bool): Whether to reconnect on failure
        """
        try:
            await super().start(token, reconnect=reconnect)
        except Exception as e:
            error_msg = f"Failed to start Discord bot: {str(e)}"
            logger.error(error_msg)
            raise DiscordError(error_msg) from e


class DiscordTool:
    def __init__(self):
        self.bot = DiscordBot()
        self._callback = None
        self.token = settings.DISCORD_BOT_TOKEN
        self.channel_id = settings.DISCORD_CHANNEL_ID

    async def initialize_bot(self) -> None:
        """Initialize and connect the Discord bot."""
        try:
            await self.bot.start(self.token)
        except Exception as e:
            error_msg = f"Failed to initialize Discord bot: {str(e)}"
            logger.error(error_msg)
            raise DiscordError(error_msg) from e

    async def add_reaction(self, channel_id: int, message_id: int, emoji: str) -> bool:
        """
        Add a reaction to a specific message.

        Args:
            channel_id (int): ID of the channel containing the message
            message_id (int): ID of the message to react to
            emoji (str): Emoji to react with (Unicode emoji or custom emoji ID)

        Returns:
            bool: True if reaction was added successfully
        """
        try:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                raise DiscordError(f"Channel {channel_id} not found")
            
            # Type check for channels that support fetch_message
            if not isinstance(channel, (discord.TextChannel, discord.Thread)):
                raise DiscordError(f"Channel type {type(channel)} does not support messages")
            
            message = await channel.fetch_message(message_id)
            await message.add_reaction(emoji)
            logger.debug(f"Reaction {emoji} added to message {message_id}")
            return True
            
        except Exception as e:
            error_msg = f"Failed to add reaction: {str(e)}"
            logger.error(error_msg)
            raise DiscordError(error_msg) from e

    async def listen_to_messages(self, channel_id: int, callback: Callable) -> None:
        """
        Listen for messages in a specific channel.

        Args:
            channel_id (int): ID of the channel to monitor
            callback (Callable): Function to handle received messages
        """
        self._callback = callback

        @self.bot.event
        async def on_message(message):
            if message.channel.id == channel_id and not message.author.bot:
                try:
                    message_data = {"username": message.author.name, "content": message.content}
                    await callback(message_data)
                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")

        @self.bot.event
        async def on_reaction_add(reaction, user):
            if reaction.message.channel.id == channel_id and not user.bot:
                try:
                    reaction_data = {
                        "message_id": reaction.message.id,
                        "emoji": str(reaction.emoji),
                        "user_id": user.id,
                        "username": user.name,
                    }
                    if hasattr(self, "_reaction_callback"):
                        await self._reaction_callback(reaction_data)
                except Exception as e:
                    logger.error(f"Error processing reaction: {str(e)}")

        logger.info(f"Started listening to messages in channel {channel_id}")

    async def send_message(self, channel_id: int, content: str) -> Optional[int]:
        """
        Send a message to a specific channel.

        Args:
            channel_id (int): ID of the channel to send message to
            content (str): Message content to send

        Returns:
            Optional[int]: Message ID if successful
        """
        try:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                raise DiscordError(f"Channel {channel_id} not found")
            
            # Type check for channels that support send
            if not isinstance(channel, (discord.TextChannel, discord.Thread)):
                raise DiscordError(f"Channel type {type(channel)} does not support sending messages")
            
            message = await channel.send(content)
            logger.debug(f"Message sent successfully to Discord with ID: {message.id}")
            return message.id
            
        except Exception as e:
            error_msg = f"Failed to send message to Discord: {str(e)}"
            logger.error(error_msg)
            raise DiscordError(error_msg) from e

    async def set_reaction_callback(self, callback: Callable) -> None:
        """
        Set a callback for reaction events.

        Args:
            callback (Callable): Function to handle received reactions
        """
        self._reaction_callback = callback
