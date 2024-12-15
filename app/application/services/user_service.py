import uuid

from app.application.interfaces.uow import UnitOfWorkFactory
from app.domain.user import User, UserId


class UserService:
    def __init__(
        self,
        unit_of_work_factory: UnitOfWorkFactory,
    ) -> None:
        self.unit_of_work_factory = unit_of_work_factory

    async def sign_up_user(self, user_id: uuid.UUID, email: str) -> None:
        uow = self.unit_of_work_factory.create()
        async with uow:
            user = User(
                id=UserId(user_id),
                email=email,
            )
            uow.users.add(user)
            await uow.commit()
