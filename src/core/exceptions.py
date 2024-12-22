"""Custom exceptions for the application."""


class AgentBaseError(Exception):
    """Base exception for Agent project."""

    pass


class DatabaseError(AgentBaseError):
    """Custom exception for database errors."""

    pass


class OAIError(AgentBaseError):
    """Custom exception for OAI errors."""

    pass


class TelegramPostError(AgentBaseError):
    """Custom exception for Telegram posting errors."""

    pass


class TwitterPostError(AgentBaseError):
    """Exception raised when posting to Twitter fails."""

    pass


class APIError(AgentBaseError):
    """Exception raised when API request fails."""

    pass
