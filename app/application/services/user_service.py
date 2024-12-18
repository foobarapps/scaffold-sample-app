import uuid

from app.application.interfaces import (
    NotificationService,
    TaskManager,
    UnitOfWorkFactory,
)
from app.domain.user import User, UserId


class UserService:
    def __init__(
        self,
        unit_of_work_factory: UnitOfWorkFactory,
        notification_service: NotificationService,
        task_manager: TaskManager,
    ) -> None:
        self.unit_of_work_factory = unit_of_work_factory
        self.notification_service = notification_service
        self.task_manager = task_manager

    async def sign_up_user(self, user_id: uuid.UUID, email: str) -> None:
        uow = self.unit_of_work_factory.create()
        async with uow:
            user = User(
                id=UserId(user_id),
                email=email,
            )
            uow.users.add(user)
            await uow.commit()

            self.task_manager.run_task(self.notification_service.send_welcome_message, email)
