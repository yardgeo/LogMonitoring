from asyncio import Queue
from datetime import datetime

from consumers import CommonNotificationConsumer
from dto import LogLineDto, NotificationDto, NotificationLevelDto

from hadnlers import LogLineHandler
from config import Config
from hadnlers.stats import TrafficStatsHandlerState


class TrafficStatsHandler(LogLineHandler):

    def __init__(self,
                 notification_consumer: CommonNotificationConsumer,
                 log_handler_queue: Queue):
        super().__init__(log_handler_queue=log_handler_queue, notification_consumer=notification_consumer)

        self._next_notification_unix_time = 0

        self._state = TrafficStatsHandlerState()

    async def consume(self, log_line: LogLineDto) -> None:
        # check if interval is finished
        if self._next_notification_unix_time < log_line.unix_time:
            #  send notification if state is not empty
            if 0 < self._next_notification_unix_time:
                await self._send_stats_notification(self._next_notification_unix_time)

            # clear stats state and update notification time
            self._clear_state(log_line.unix_time)

        # update current stats state
        self._update_state(log_line)

    def _clear_state(self, current_unix_time: int) -> None:
        # update next notification time
        self._next_notification_unix_time = current_unix_time + Config.TRAFFIC_STATS_TIME_INTERVAL

        # clear state
        self._state.clear()

    def _update_state(self, log_line: LogLineDto) -> None:
        self._state.update(log_line)

    async def _send_stats_notification(self, current_unix_time: int):
        # send message to async queue so write can write the message
        await self.notification_consumer.consume_notification(
            NotificationDto(
                level=NotificationLevelDto(Config.TRAFFIC_STATS_NOTIFICATION_LEVEL),
                type=Config.TRAFFIC_STATS_NOTIFICATION_TYPE,
                message=Config.TRAFFIC_STATS_NOTIFICATION_MESSAGE.format(
                    time=datetime.utcfromtimestamp(current_unix_time).strftime(Config.DATETIME_FORMAT),
                    stats=self._state.get_notification_message()
                )
            )
        )
