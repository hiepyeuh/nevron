"""Custom exceptions for the application."""


class AgentBaseError(Exception):
    """Base exception for Agent project."""

    pass


class MemoryError(AgentBaseError):
    """Custom exception for memory errors."""

    pass


class OAIError(AgentBaseError):
    """Custom exception for OAI errors."""

    pass


class TelegramError(AgentBaseError):
    """Custom exception for Telegram posting errors."""

    pass


class TwitterError(AgentBaseError):
    """Exception raised when posting to Twitter fails."""

    pass


class APIError(AgentBaseError):
    """Exception raised when API request fails."""

    pass
