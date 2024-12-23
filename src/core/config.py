from enum import Enum
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(Enum):
    """The environment of the application."""

    PRODUCTION = "production"
    DEVELOPMENT = "development"
    CI = "ci"


class Settings(BaseSettings):
    """Settings for the autonomous agent."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )

    # === General settings ===

    #: Environment (Production, Development, CI)
    ENVIRONMENT: Environment = Environment.PRODUCTION

    #: Project name
    PROJECT_NAME: str = "autonomous-agent"

    #: Path to the persistent Q-table file
    PERSISTENT_Q_TABLE_PATH: str = "persistent_q_table.json"

    # === OpenAI settings ===

    #: OpenAI API key
    OPENAI_API_KEY: str = ""

    #: OpenAI model
    OPENAI_MODEL: str = "gpt-4o-mini"

    # === Perplexity settings ===

    #: Perplexity API key
    PERPLEXITY_API_KEY: str = ""

    #: Perplexity endpoint
    PERPLEXITY_ENDPOINT: str = ""

    # === Telegram settings ===

    #: Telegram bot token
    TELEGRAM_BOT_TOKEN: str = ""

    #: Telegram chat ID for main channel/group
    TELEGRAM_CHAT_ID: str = ""

    #: Telegram admin chat ID for administrative messages
    TELEGRAM_ADMIN_CHAT_ID: str = ""

    #: Telegram reviewer chat IDs for content review
    TELEGRAM_REVIEWER_CHAT_IDS: List[str] = []

    # === Twitter settings ===

    #: Twitter API key
    TWITTER_API_KEY: str = ""

    #: Twitter API secret key
    TWITTER_API_SECRET_KEY: str = ""

    #: Twitter access token
    TWITTER_ACCESS_TOKEN: str = ""

    #: Twitter access token secret
    TWITTER_ACCESS_TOKEN_SECRET: str = ""

    # ==== Validators ====

    @field_validator("ENVIRONMENT", mode="before")
    def validate_environment(cls, value: str | Environment) -> Environment:
        """Validate and convert the environment value."""
        if isinstance(value, Environment):
            return value
        try:
            return Environment(value.lower())
        except ValueError:
            raise ValueError(
                f"Invalid environment value: {value}. Must be one of {list(Environment)}"
            )

    @field_validator("TELEGRAM_REVIEWER_CHAT_IDS", mode="before")
    def parse_reviewer_chat_ids(cls, value: str | List[str]) -> List[str]:
        """Ensure TELEGRAM_REVIEWER_CHAT_IDS is parsed as a list."""
        if isinstance(value, str):
            return [chat_id.strip() for chat_id in value.split(",") if chat_id.strip()]
        return value


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")  # type: ignore[call-arg]
