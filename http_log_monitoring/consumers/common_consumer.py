from abc import ABC, abstractmethod

from dto import NotificationDto


class CommonConsumer(ABC):

    @abstractmethod
    async def consume_message(self, notification: NotificationDto) -> None:
        raise NotImplementedError("")

    @abstractmethod
    async def start(self) -> None:
        raise NotImplementedError("")
