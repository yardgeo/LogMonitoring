from abc import ABC, abstractmethod
from typing import AsyncIterable

from dto import LogLineDto


class HttpLogProducer(ABC):
    """
    A class to represent http log producer from a specific source.
    """

    @abstractmethod
    async def stream_logs(self) -> AsyncIterable[LogLineDto]:
        """
        Stream logs form the source
        :return: Generator of log lines
        :rtype: AsyncIterable[LogLineDto]
        """
        raise NotImplementedError("")

    @abstractmethod
    async def start(self) -> None:
        """
        Start producer
        """
        raise NotImplementedError("")
