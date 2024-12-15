import abc
import dataclasses
from typing import override

from .base import Entity, EntityId


@dataclasses.dataclass(frozen=True)
class UserId(EntityId):
    pass


class User(Entity):
    def __init__(
        self,
        id: UserId,
        email: str,
    ) -> None:
        self._id = id
        self._email = email

    @override
    @property
    def id(self) -> UserId:
        return self._id

    @property
    def email(self) -> str:
        return self._email


class UserRepository(abc.ABC):
    @abc.abstractmethod
    async def get(self, id: UserId) -> User | None:
        pass

    @abc.abstractmethod
    def add(self, user: User) -> None:
        pass
