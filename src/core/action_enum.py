from enum import Enum


class AgentAction(Enum):
    IDLE = "idle"
    CHECK_NEWS = "check_news"
    POST_TO_TELEGRAM = "post_to_telegram"
    POST_TO_TWITTER = "post_to_twitter"
