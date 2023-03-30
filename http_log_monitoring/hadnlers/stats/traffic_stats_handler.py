import asyncio
from collections import deque
from datetime import datetime

from dto import LogLineDto

from hadnlers import LogLineHandler
from config import Config


class TrafficStatsHandler(LogLineHandler):
    def __init__(self, message_queue: asyncio.Queue):
        super().__init__(message_queue)

        # queue for last {time} logs
        self._log_queue = deque()

    async def handle(self, log_line: LogLineDto) -> None:
        # remove all elements from queue which are older than alert range
        while len(self._log_queue) > 0 and self._log_queue[0] < log_line.unix_time - Config.HIGH_TRAFFIC_TIME_INTERVAL:
            self._log_queue.popleft()

        # append current log time
        self._log_queue.append(log_line.unix_time)

        # check if should trigger
        if len(self._log_queue) > Config.HIGH_TRAFFIC_MAX_REQUESTS_PER_SECOND * Config.HIGH_TRAFFIC_TIME_INTERVAL:
            await self.message_queue.put(
                Config.HIGH_TRAFFIC_ALERT_MESSAGE.format(
                    time=datetime.utcfromtimestamp(log_line.unix_time).strftime(Config.DATETIME_FORMAT),
                    value=len(self._log_queue)
                )
            )




