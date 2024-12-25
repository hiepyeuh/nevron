from enum import Enum


class AgentState(Enum):
    DEFAULT = "default"
    IDLE = "idle"
    WAITING_FOR_NEWS = "waiting_for_news"
    JUST_POSTED_TO_TELEGRAM = "just_posted_to_telegram"
    JUST_POSTED_TO_TWITTER = "just_posted_to_twitter"
