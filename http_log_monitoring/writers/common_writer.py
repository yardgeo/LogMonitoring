from abc import ABC, abstractmethod
from asyncio import Queue


class CommonWriter(ABC):
    def __init__(self,
                 message_queue: Queue):
        self.message_queue = message_queue

    @abstractmethod
    async def write(self, msg: str) -> None:
        raise NotImplementedError("")

    @abstractmethod
    async def run(self) -> None:
        raise NotImplementedError("")
