from dataclasses import dataclass
from enum import Enum


class NotificationLevelDto(Enum):
    INFO = "INFO"
    CRITICAL = "CRITICAL"


@dataclass
class NotificationDto:
    message: str
    level: NotificationLevelDto
    type: str
