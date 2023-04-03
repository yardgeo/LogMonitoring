from asyncio import Queue
from collections import deque

from config import Config
from consumers import CommonNotificationConsumer
from dto import LogLineDto, NotificationDto, NotificationLevelDto
from hadnlers.log_line_handler import LogLineHandler

from utils import format_unix_time

# constants
TIME_INTERVAL = Config.HIGH_TRAFFIC_TIME_INTERVAL
MAX_REQUESTS_PER_SECOND = Config.HIGH_TRAFFIC_MAX_REQUESTS_PER_SECOND
MAX_REQUESTS_PER_INTERVAL = Config.HIGH_TRAFFIC_MAX_REQUESTS_PER_INTERVAL
ALERT_NOTIFICATION_MESSAGE = Config.HIGH_TRAFFIC_ALERT_NOTIFICATION_MESSAGE
RECOVERY_NOTIFICATION_MESSAGE = Config.\
    HIGH_TRAFFIC_RECOVERY_NOTIFICATION_MESSAGE
ALERT_NOTIFICATION_LEVEL = Config.HIGH_TRAFFIC_ALERT_NOTIFICATION_LEVEL
ALERT_NOTIFICATION_TYPE = Config.HIGH_TRAFFIC_ALERT_NOTIFICATION_TYPE
RECOVERY_NOTIFICATION_LEVEL = Config.HIGH_TRAFFIC_RECOVERY_NOTIFICATION_LEVEL
RECOVERY_NOTIFICATION_TYPE = Config.HIGH_TRAFFIC_RECOVERY_NOTIFICATION_TYPE


class HighTrafficAlertHandler(LogLineHandler):
    """
    A class to represent a handler for high traffic notifications
    """

    def __init__(self,
                 notification_consumer: CommonNotificationConsumer,
                 log_handler_queue: Queue):
        super().__init__(log_handler_queue=log_handler_queue,
                         notification_consumer=notification_consumer)

        # queue for last {time} logs
        self._log_queue = deque()

        # set high traffic flag to avoid duplicate alerts
        self._high_traffic = False

    async def consume(self, log_line: LogLineDto) -> None:
        # get left time border
        border_time = log_line.unix_time - TIME_INTERVAL

        # remove all elements from the queue which are older than alert range
        while len(self._log_queue) > 0 and self._log_queue[0] < border_time:
            self._log_queue.popleft()

        # append current log time
        self._log_queue.append(log_line.unix_time)

        # get queue length
        n = len(self._log_queue)

        # check if traffic exceed the limit
        if not self._high_traffic and n > MAX_REQUESTS_PER_INTERVAL:
            await self._send_high_traffic_notification(log_line.unix_time)

        # check if traffic was high but now is returned to normal
        elif self._high_traffic and n <= MAX_REQUESTS_PER_INTERVAL:
            await self._send_recovery_notification(log_line.unix_time)

    async def _send_high_traffic_notification(self, current_unix_time: int):
        # send message to async queue so write can write the message
        await self.notification_consumer.consume_notification(
            NotificationDto(
                level=NotificationLevelDto(ALERT_NOTIFICATION_LEVEL),
                type=ALERT_NOTIFICATION_TYPE,
                message=ALERT_NOTIFICATION_MESSAGE.format(
                    time=format_unix_time(current_unix_time),
                    value=len(self._log_queue)
                )
            )
        )

        # set high traffic flag to True
        self._high_traffic = True

    async def _send_recovery_notification(self, current_unix_time: int):
        # send message to async queue so write can write the message
        await self.notification_consumer.consume_notification(
            NotificationDto(
                level=NotificationLevelDto(RECOVERY_NOTIFICATION_LEVEL),
                type=RECOVERY_NOTIFICATION_TYPE,
                message=RECOVERY_NOTIFICATION_MESSAGE.format(
                    time=format_unix_time(current_unix_time),
                )
            )
        )

        # set high traffic flag to False
        self._high_traffic = False
