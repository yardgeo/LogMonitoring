import asyncio

from consumers import ConsoleNotificationConsumer
from hadnlers import HighTrafficAlertHandler, TrafficStatsHandler
from producers import LocalCSVFileHttpLogProducer


class Dispatcher:
    def __init__(self,
                 log_file_path: str):
        self._loop = asyncio.get_event_loop()
        self._producer = LocalCSVFileHttpLogProducer(log_file_path)
        self._notification_consumer = ConsoleNotificationConsumer()
        self._handlers = [
            HighTrafficAlertHandler(
                notification_consumer=self._notification_consumer,
                log_handler_queue=asyncio.Queue(loop=self._loop)
            ),
            TrafficStatsHandler(
                notification_consumer=self._notification_consumer,
                log_handler_queue=asyncio.Queue(loop=self._loop))
        ]

    async def _handle_logs(self):
        async for log_line in self._producer.stream_logs():
            for handler in self._handlers:
                await handler.handle(log_line)

    def _close_all(self):
        try:
            to_cancel = asyncio.all_tasks(self._loop)
            if not to_cancel:
                return
            # cancel all tasks
            for task in to_cancel:
                task.cancel()

            self._loop.run_until_complete(
                asyncio.gather(*to_cancel, loop=self._loop, return_exceptions=True))

            for task in to_cancel:
                if task.cancelled():
                    continue
                if task.exception() is not None:
                    self._loop.call_exception_handler({
                        'message': 'unhandled exception during test shutdown',
                        'exception': task.exception(),
                        'task': task,
                    })
            # shutdown asyncgens
            self._loop.run_until_complete(self._loop.shutdown_asyncgens())
        finally:
            asyncio.set_event_loop(None)
            self._loop.close()

    def _start_all(self):
        tasks = [self._producer.start, self._notification_consumer.start, self._handle_logs]
        tasks.extend([handler.start for handler in self._handlers])
        # async with asyncio.TaskGroup() as tg:
        #     for task in tasks:
        #         tg.create_task(task())
        try:
            self._loop.run_until_complete(
                asyncio.gather(
                    *[task() for task in tasks],
                    return_exceptions=True
                )
            )
        finally:
            self._close_all()

    def run(self):
        self._start_all()
