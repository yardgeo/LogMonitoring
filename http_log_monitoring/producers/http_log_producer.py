from abc import ABC, abstractmethod
from typing import Iterable, AsyncIterable

from dto import LogLineDto


class HttpLogProducer(ABC):

    @abstractmethod
    async def stream_logs(self) -> AsyncIterable[LogLineDto]:
        raise NotImplementedError("")

    @abstractmethod
    async def start(self) -> None:
        raise NotImplementedError("")
