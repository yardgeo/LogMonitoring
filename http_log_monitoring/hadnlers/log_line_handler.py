import asyncio
from abc import ABC, abstractmethod
from asyncio import Queue, Condition

from consumers import CommonConsumer
from dto import LogLineDto


class LogLineHandler(ABC):

    def __init__(self,
                 log_handler_queue: Queue,
                 consumer: CommonConsumer):
        self.consumer = consumer
        self.log_handler_queue = log_handler_queue

    async def handle(self, log_line: LogLineDto) -> None:
        await self.log_handler_queue.put(log_line)

    async def start(self) -> None:
        print(f"Handler {self.__class__} started")
        while True:
            log_line = await self.log_handler_queue.get()
            await self.consume(log_line)

    @abstractmethod
    async def consume(self, log_line: LogLineDto) -> None:
        raise NotImplementedError("")