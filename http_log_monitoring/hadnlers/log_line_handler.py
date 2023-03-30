import asyncio
from abc import ABC, abstractmethod

from dto import LogLineDto


class LogLineHandler(ABC):

    def __init__(self,
                 message_queue: asyncio.Queue):
        self.message_queue = message_queue

    @abstractmethod
    async def handle(self, log_line: LogLineDto) -> None:
        raise NotImplementedError("")
