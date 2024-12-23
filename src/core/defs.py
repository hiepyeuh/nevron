"""Here will be all the definitions of the core components of the system"""

from enum import Enum


class Environment(Enum):
    """The environment of the application."""

    PRODUCTION = "production"
    DEVELOPMENT = "development"
    CI = "ci"
