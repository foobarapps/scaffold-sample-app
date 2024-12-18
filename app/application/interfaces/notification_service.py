import abc


class NotificationService(abc.ABC):
    @abc.abstractmethod
    async def send_welcome_message(self, email: str) -> None: ...
