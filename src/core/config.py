from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.defs import Environment


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

    #: PlanningModule parameters
    PLANNING_ALPHA: float = 0.1  # Default learning rate
    PLANNING_GAMMA: float = 0.95  # Default discount factor
    PLANNING_EPSILON: float = 0.1  # Default exploration rate

    #: Memory module configuration
    MEMORY_COLLECTION_NAME: str = "agent_memory"
    MEMORY_HOST: str = "localhost"
    MEMORY_PORT: int = 6333
    MEMORY_VECTOR_SIZE: int = 1536

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

    def validate_memory_settings(self, params, required_params):
        """Validate the settings."""
        for param, param_type in required_params.items():
            if param not in params:
                raise ValueError(f"{param} is required.")
            if not isinstance(params[param], param_type):
                raise ValueError(f"{param} must be of type {param_type.__name__}.")


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")  # type: ignore[call-arg]
