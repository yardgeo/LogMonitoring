import asyncio

from consumers import ConsoleConsumer
from hadnlers import HighTrafficAlertHandler, TrafficStatsHandler
from producers import LocalCSVFileHttpLogProducer


class Dispatcher:
    def __init__(self,
                 log_file_path: str):
        self._loop = asyncio.get_event_loop()
        self._producer = LocalCSVFileHttpLogProducer(log_file_path)
        self._consumer = ConsoleConsumer()
        self._handlers = [
            HighTrafficAlertHandler(consumer=self._consumer, log_handler_queue=asyncio.Queue(loop=self._loop)),
            TrafficStatsHandler(consumer=self._consumer, log_handler_queue=asyncio.Queue(loop=self._loop))
        ]

    async def _handle_logs(self):
        async for log_line in self._producer.stream_logs():
            for handler in self._handlers:
                await handler.handle(log_line)
            await asyncio.sleep(1e-9)

    def _start_all(self):
        tasks = [self._producer.start, self._consumer.start, self._handle_logs]
        tasks.extend([handler.start for handler in self._handlers])
        # async with asyncio.TaskGroup() as tg:
        #     for task in tasks:
        #         tg.create_task(task())
        self._loop.run_until_complete(
            asyncio.gather(
                *[task() for task in tasks]
                # return_exceptions=True
            )
        )

    def run(self):
        self._start_all()
