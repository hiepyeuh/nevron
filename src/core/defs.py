"""Here will be all the definitions of the core components of the system"""

from enum import Enum


class Environment(Enum):
    """The environment of the application."""

    PRODUCTION = "production"
    DEVELOPMENT = "development"
    CI = "ci"


class AgentAction(Enum):
    """The actions that the agent can take."""

    IDLE = "idle"
    CHECK_NEWS = "check_news"
    POST_TO_TELEGRAM = "post_to_telegram"
    POST_TO_TWITTER = "post_to_twitter"


class AgentState(Enum):
    """The states that the agent can be in."""

    DEFAULT = "default"
    IDLE = "idle"
    WAITING_FOR_NEWS = "waiting_for_news"
    JUST_POSTED_TO_TELEGRAM = "just_posted_to_telegram"
    JUST_POSTED_TO_TWITTER = "just_posted_to_twitter"
