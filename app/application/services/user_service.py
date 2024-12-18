from app.application.interfaces import (
    NotificationService,
    TaskManager,
)


class UserService:
    def __init__(
        self,
        notification_service: NotificationService,
        task_manager: TaskManager,
    ) -> None:
        self.notification_service = notification_service
        self.task_manager = task_manager

    async def send_welcome_message(self, email: str) -> None:
        self.task_manager.run_task(self.notification_service.send_welcome_message, email)
