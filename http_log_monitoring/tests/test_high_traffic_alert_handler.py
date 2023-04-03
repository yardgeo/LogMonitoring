import asyncio
import random
from datetime import datetime
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from config import Config
from consumers import ConsoleNotificationConsumer
from dto import LogLineDto, NotificationDto, NotificationLevelDto
from hadnlers import HighTrafficAlertHandler

# constants
TIME_INTERVAL = Config.HIGH_TRAFFIC_TIME_INTERVAL
MAX_REQUESTS_PER_SECOND = Config.HIGH_TRAFFIC_MAX_REQUESTS_PER_SECOND
MAX_REQUESTS_PER_INTERVAL = Config.HIGH_TRAFFIC_MAX_REQUESTS_PER_INTERVAL
ALERT_NOTIFICATION_MESSAGE = Config.HIGH_TRAFFIC_ALERT_NOTIFICATION_MESSAGE
RECOVERY_NOTIFICATION_MESSAGE = Config. \
    HIGH_TRAFFIC_RECOVERY_NOTIFICATION_MESSAGE
ALERT_NOTIFICATION_LEVEL = Config.HIGH_TRAFFIC_ALERT_NOTIFICATION_LEVEL
ALERT_NOTIFICATION_TYPE = Config.HIGH_TRAFFIC_ALERT_NOTIFICATION_TYPE
RECOVERY_NOTIFICATION_LEVEL = Config.HIGH_TRAFFIC_RECOVERY_NOTIFICATION_LEVEL
RECOVERY_NOTIFICATION_TYPE = Config.HIGH_TRAFFIC_RECOVERY_NOTIFICATION_TYPE


class TestHighTrafficAlertHandler(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self._log_queue = asyncio.Queue()
        self._mock_consume_notification_f = AsyncMock()

        consumer = ConsoleNotificationConsumer()
        consumer.consume_notification = self._mock_consume_notification_f

        self._handler = HighTrafficAlertHandler(
            notification_consumer=consumer,
            log_handler_queue=self._log_queue
        )

        # schedule the coroutine to run in the background
        self._task = asyncio.create_task(self._handler.start())

        # allow the task to run
        await asyncio.sleep(0)

    async def _generate_border_traffic(self, unix_time):
        log_line = LogLineDto(
            *["10.0.0.4", "-", "apache", unix_time, "POST /report HTTP/1.0",
              404.0, 1307.0])
        traffic = (log_line for _ in
                   range(MAX_REQUESTS_PER_INTERVAL))

        # handle each hit
        for hit in traffic:
            await self._handler.handle(hit)
        # wait for handler to work
        await asyncio.sleep(1)

        # check that no notification were called
        self._mock_consume_notification_f.assert_not_called()

    async def test_high_traffic_detected(self):
        # generate traffic with maximum acceptable number of hits
        unix_time = float(random.randrange(int(1e7)))
        await self._generate_border_traffic(unix_time)

        # add next
        new_unix_time = unix_time + TIME_INTERVAL - 1
        await self._handler.handle(
            log_line=LogLineDto(*["10.0.0.4", "-", "apache", new_unix_time,
                                  "POST /report HTTP/1.0", 404.0, 1307.0])
        )
        # wait for handler to work
        await asyncio.sleep(0)

        # check that notification was created
        self._mock_consume_notification_f.assert_called_once_with(
            NotificationDto(
                message=ALERT_NOTIFICATION_MESSAGE.format(
                    time=datetime.utcfromtimestamp(new_unix_time).strftime(
                        Config.DATETIME_FORMAT),
                    value=MAX_REQUESTS_PER_INTERVAL + 1
                ),
                level=NotificationLevelDto.CRITICAL,
                type='ALERT')
        )

        self.assertTrue(self._handler._high_traffic)

    async def test_high_traffic_recovery_detected(self):
        # generate traffic with maximum acceptable number of hits
        unix_time = float(random.randrange(int(1e7)))
        await self._generate_border_traffic(unix_time)

        # add 2 next. First to generate high trafic, second for recovery
        new_unix_time = unix_time + TIME_INTERVAL - 1
        await self._handler.handle(
            log_line=LogLineDto(*["10.0.0.4", "-", "apache", new_unix_time,
                                  "POST /report HTTP/1.0", 404.0, 1307.0])
        )
        # wait for handler to work
        await asyncio.sleep(0)

        # reset mock
        self._mock_consume_notification_f.reset_mock()

        new_unix_time = 3 * unix_time + TIME_INTERVAL - 1
        await self._handler.handle(
            log_line=LogLineDto(*["10.0.0.4", "-", "apache", new_unix_time,
                                  "POST /report HTTP/1.0", 404.0, 1307.0])
        )

        # wait for handler to work
        await asyncio.sleep(0)

        # check that notification was created
        self._mock_consume_notification_f.assert_called_once_with(
            NotificationDto(
                message=RECOVERY_NOTIFICATION_MESSAGE.format(
                    time=datetime.utcfromtimestamp(new_unix_time).strftime(
                        Config.DATETIME_FORMAT)
                ),
                level=NotificationLevelDto.CRITICAL,
                type='RECOVERY')
        )

        self.assertFalse(self._handler._high_traffic)

    async def test_high_traffic_alert_sent_once(self):
        # generate traffic with maximum acceptable number of hits
        unix_time = float(random.randrange(int(1e7)))
        n = 10
        await self._generate_border_traffic(unix_time)

        # add n next
        new_unix_time = unix_time + TIME_INTERVAL - 1
        for i in range(n):
            await self._handler.handle(
                log_line=LogLineDto(*["10.0.0.4", "-", "apache", new_unix_time,
                                      "POST /report HTTP/1.0", 404.0, 1307.0])
            )
        # wait for handler to work
        await asyncio.sleep(0)

        # check that notification was created
        self._mock_consume_notification_f.assert_called_once_with(
            NotificationDto(
                message=ALERT_NOTIFICATION_MESSAGE.format(
                    time=datetime.utcfromtimestamp(new_unix_time).strftime(
                        Config.DATETIME_FORMAT),
                    value=MAX_REQUESTS_PER_INTERVAL + 1
                ),
                level=NotificationLevelDto.CRITICAL,
                type='ALERT')
        )

    async def test_high_traffic_recovery_sent_once(self):
        # generate traffic with maximum acceptable number of hits
        unix_time = float(random.randrange(int(1e7)))
        n = 10
        await self._generate_border_traffic(unix_time)

        # add 2 next. First to generate high trafic, second for recovery
        new_unix_time = unix_time + TIME_INTERVAL - 1
        await self._handler.handle(
            log_line=LogLineDto(*["10.0.0.4", "-", "apache", new_unix_time,
                                  "POST /report HTTP/1.0", 404.0, 1307.0])
        )
        # wait for handler to work
        await asyncio.sleep(0)

        # reset mock
        self._mock_consume_notification_f.reset_mock()

        new_unix_time = 3 * unix_time + TIME_INTERVAL - 1
        for i in range(n):
            await self._handler.handle(
                log_line=LogLineDto(*["10.0.0.4", "-", "apache", new_unix_time,
                                      "POST /report HTTP/1.0", 404.0, 1307.0])
            )
        # wait for handler to work
        await asyncio.sleep(0)

        # check that notification was created
        self._mock_consume_notification_f.assert_called_once_with(
            NotificationDto(
                message=RECOVERY_NOTIFICATION_MESSAGE.format(
                    time=datetime.utcfromtimestamp(new_unix_time).strftime(
                        Config.DATETIME_FORMAT)
                ),
                level=NotificationLevelDto.CRITICAL,
                type='RECOVERY')
        )
