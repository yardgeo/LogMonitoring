from dataclasses import dataclass
from enum import Enum


class NotificationLevelDto(Enum):
    """
    An enum to represent all possible levels of notification
    """
    INFO = "INFO"
    CRITICAL = "CRITICAL"


@dataclass
class NotificationDto:
    """
    A class to represent notification
    """
    message: str
    level: NotificationLevelDto
    type: str
