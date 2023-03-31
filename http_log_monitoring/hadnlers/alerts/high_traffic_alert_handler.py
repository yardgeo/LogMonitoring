import asyncio
from asyncio import Queue, Event
from collections import deque
from datetime import datetime

from consumers import CommonConsumer
from dto import LogLineDto, NotificationDto, NotificationLevelDto

from hadnlers import LogLineHandler
from config import Config


class HighTrafficAlertHandler(LogLineHandler):
    def __init__(self,
                 consumer: CommonConsumer,
                 log_handler_queue: Queue):
        super().__init__(log_handler_queue=log_handler_queue, consumer=consumer)

        # queue for last {time} logs
        self._log_queue = deque()

        # set high traffic flag to avoid duplicate alerts
        self._high_traffic = False

    async def consume(self, log_line: LogLineDto) -> None:
        # remove all elements from queue which are older than alert range
        while len(self._log_queue) > 0 and self._log_queue[0] < log_line.unix_time - Config.HIGH_TRAFFIC_TIME_INTERVAL:
            self._log_queue.popleft()

        # append current log time
        self._log_queue.append(log_line.unix_time)

        # check if traffic exceed the limit
        if not self._high_traffic and len(self._log_queue) > Config.HIGH_TRAFFIC_MAX_REQUESTS_PER_INTERVAL:
            await self._send_high_traffic_message(log_line.unix_time)

        # check if traffic was high but now is returned to normal
        elif self._high_traffic and len(self._log_queue) <= Config.HIGH_TRAFFIC_MAX_REQUESTS_PER_INTERVAL:
            await self._send_recovery_message(log_line.unix_time)
        # await asyncio.sleep(2)

    async def _send_high_traffic_message(self, current_unix_time: int):
        # send message to async queue so write can write the message
        await self.consumer.consume_message(
            NotificationDto(
                level=NotificationLevelDto(Config.HIGH_TRAFFIC_ALERT_NOTIFICATION_LEVEL),
                type=Config.HIGH_TRAFFIC_ALERT_NOTIFICATION_TYPE,
                message=Config.HIGH_TRAFFIC_ALERT_NOTIFICATION_MESSAGE.format(
                    time=datetime.utcfromtimestamp(current_unix_time).strftime(Config.DATETIME_FORMAT),
                    value=len(self._log_queue)
                )
            )
        )

        # set high traffic flag to True
        self._high_traffic = True

    async def _send_recovery_message(self, current_unix_time: int):
        # send message to async queue so write can write the message
        await self.consumer.consume_message(
            NotificationDto(
                level=NotificationLevelDto(Config.HIGH_TRAFFIC_RECOVERY_NOTIFICATION_LEVEL),
                type=Config.HIGH_TRAFFIC_RECOVERY_NOTIFICATION_TYPE,
                message=Config.HIGH_TRAFFIC_RECOVERY_NOTIFICATION_MESSAGE.format(
                    time=datetime.utcfromtimestamp(current_unix_time).strftime(Config.DATETIME_FORMAT),
                )
            )
        )

        # set high traffic flag to False
        self._high_traffic = False
