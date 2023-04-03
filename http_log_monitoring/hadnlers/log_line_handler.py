import logging
from abc import ABC, abstractmethod
from asyncio import Queue

from consumers import CommonNotificationConsumer
from dto import LogLineDto


class LogLineHandler(ABC):
    """
    A class to represent abstract log line handler,
     which process log line based on the specific rules
      and generate notifications for consumer.
    """

    def __init__(self,
                 log_handler_queue: Queue,
                 notification_consumer: CommonNotificationConsumer):
        self.notification_consumer = notification_consumer
        self.log_handler_queue = log_handler_queue
        self.logger = logging.getLogger()

    async def handle(self, log_line: LogLineDto) -> None:
        """
        Handle log line and put to log queue for processing.
        :param log_line: line of log
        :type log_line: LogLineDto
        """
        await self.log_handler_queue.put(log_line)

    async def join(self) -> None:
        """
        Join consumer-producer queue for handler
        """
        await self.log_handler_queue.join()

    async def start(self) -> None:
        """
        Start handler, which process log lines.
        """
        # print starting message
        self.logger.debug(f"Handler {self.__class__} started")

        # run infinite loop, process new log line from queue and consume it
        while True:
            # get log line from queue
            log_line = await self.log_handler_queue.get()

            # consume log line
            await self.consume(log_line)

            # notify the queue that the "log line" has been processed
            self.log_handler_queue.task_done()

    @abstractmethod
    async def consume(self, log_line: LogLineDto) -> None:
        """
        Consume a single line of log,
        process it and generate notification if needed.
        :param log_line: line of log
        :type log_line: LogLineDto
        """
        raise NotImplementedError("")
