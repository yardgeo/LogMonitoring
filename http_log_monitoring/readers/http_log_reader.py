from abc import ABC, abstractmethod

from dto import LogLineDto


class HttpLogReader(ABC):

    @abstractmethod
    async def read_line(self) -> LogLineDto:
        pass
