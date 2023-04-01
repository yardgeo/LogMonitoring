import asyncio
import random
import time
from unittest import TestCase
from unittest.mock import AsyncMock

from config import Config
from consumers import ConsoleNotificationConsumer
from dto import LogLineDto
from hadnlers import TrafficStatsHandler


class TestTrafficStatsHandler(TestCase):
    async def asyncSetUp(self) -> None:
        self._log_queue = asyncio.Queue()
        self._mock_consume_notification_function = AsyncMock()

        consumer = ConsoleNotificationConsumer()
        consumer.consume_notification = self._mock_consume_notification_function

        self._handler = TrafficStatsHandler(notification_consumer=consumer, log_handler_queue=self._log_queue)

        # schedule the coroutine to run in the background
        self._task = asyncio.create_task(self._handler.start())

        # allow the task to run
        await asyncio.sleep(0)

    async def _generate_random_logs_with_size_n(self, seconds: int):
        start = int(time.time())
        while int(time.time()) < start + seconds:
            log_line = LogLineDto(*["10.0.0.4", "-", "apache", int(time.time()), "POST /report HTTP/1.0",
                                    random.randint(199, 520), random.randint(20, 2000)])
            await self._handler.handle(log_line)
            await asyncio.sleep(random.uniform(0, 1))

    async def test_stats_produced_regularly(self):
        n = 32
        await self._generate_random_logs_with_size_n(n)
        self.assertEqual(n // Config.TRAFFIC_STATS_TIME_INTERVAL,
                         self._mock_consume_notification_function.call_count)
