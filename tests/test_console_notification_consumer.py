import asyncio
from unittest import IsolatedAsyncioTestCase

from consumers import ConsoleNotificationConsumer
from dto import NotificationDto, NotificationLevelDto


class TestConsoleNotificationConsumer(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self._console_notification_consumer = ConsoleNotificationConsumer()

    async def _assert_log_output(self, notification: NotificationDto, expected_output: str):
        # mock all logs with ctx
        with self.assertLogs() as ctx:
            await self._console_notification_consumer.consume_notification(notification)

        # check if only one raw was written
        self.assertEqual(len(ctx.output), 1)

        # check output
        self.assertEqual(ctx.output[0], expected_output)

    async def test_consume_notification_info_level(self):
        msg = "test"
        expected_output = f"INFO:root:test"
        notification = NotificationDto(message=msg, level=NotificationLevelDto.INFO, type="any")
        await self._assert_log_output(notification=notification, expected_output=expected_output)

    async def test_consume_notification_critical_level(self):
        msg = "test"
        expected_output = f"CRITICAL:root:test"
        notification = NotificationDto(message=msg, level=NotificationLevelDto.CRITICAL, type="any")
        await self._assert_log_output(notification=notification, expected_output=expected_output)

    async def test_start_doing_nothing(self):
        # get number of running tasks
        num_of_running_tasks = len(asyncio.all_tasks())

        # schedule the coroutine to run in the background
        asyncio.create_task(self._console_notification_consumer.start())

        # allow the task to run
        await asyncio.sleep(0)

        # check that number of running tasks wasn't changed
        self.assertEqual(len(asyncio.all_tasks()), num_of_running_tasks)
