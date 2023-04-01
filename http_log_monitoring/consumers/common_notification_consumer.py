from abc import ABC, abstractmethod

from dto import NotificationDto


class CommonNotificationConsumer(ABC):

    @abstractmethod
    async def consume_notification(self, notification: NotificationDto) -> None:
        raise NotImplementedError("")

    @abstractmethod
    async def start(self) -> None:
        raise NotImplementedError("")
