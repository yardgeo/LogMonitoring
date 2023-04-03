import logging
import sys

from consumers import CommonNotificationConsumer
from dto import NotificationDto, NotificationLevelDto
from utils import CustomLoggerFormatter


class ConsoleNotificationConsumer(CommonNotificationConsumer):
    """
    A class to represent Console notification consumer.
    Consumer process notification and log it to standard console.
    """

    def __init__(self):
        # configure console output format
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.INFO)

        # add handler, highlight error and critical messages with red
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        handler.setFormatter(CustomLoggerFormatter())

        # set handler
        self._logger.addHandler(handler)

    async def consume_notification(self,
                                   notification: NotificationDto) -> None:
        # logging info
        if notification.level == NotificationLevelDto.INFO:
            self._logger.info(notification.message)

        # logging critical
        elif notification.level == NotificationLevelDto.CRITICAL:
            self._logger.critical(notification.message)

    async def start(self) -> None:
        pass
