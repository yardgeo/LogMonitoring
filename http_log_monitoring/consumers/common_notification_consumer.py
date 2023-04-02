from abc import ABC, abstractmethod

from dto import NotificationDto


class CommonNotificationConsumer(ABC):
    """
    A class to represent notification consumer
    """

    @abstractmethod
    async def consume_notification(self, notification: NotificationDto) -> None:
        """
        Consume and process notification data for notification, visualization or logging pipelines
        :param notification: notification object
        :type notification: NotificationDto
        """
        raise NotImplementedError("")

    @abstractmethod
    async def start(self) -> None:
        """
        Start consumer
        """
        raise NotImplementedError("")
