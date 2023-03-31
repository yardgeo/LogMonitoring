import logging
import sys

from consumers import CommonConsumer
from utils import CustomLoggerFormatter
from dto import NotificationDto, NotificationLevelDto


class ConsoleConsumer(CommonConsumer):
    def __init__(self):
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(CustomLoggerFormatter())
        self._logger.addHandler(handler)

    async def consume_message(self, notification: NotificationDto) -> None:
        if notification.level == NotificationLevelDto.INFO:
            self._logger.info(notification.message)
        elif notification.level == NotificationLevelDto.CRITICAL:
            self._logger.critical(notification.message)

    async def start(self) -> None:
        pass
