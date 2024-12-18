import abc
import dataclasses
import datetime
from collections.abc import Sequence
from typing import override

from .base import Entity, EntityId


@dataclasses.dataclass(frozen=True)
class MessageId(EntityId):
    pass


@dataclasses.dataclass(frozen=True)
class UserId(EntityId):
    pass


class Message(Entity):
    def __init__(
        self,
        id: MessageId,
        user_id: UserId,
        content: str,
        sent_at: datetime.datetime,
    ) -> None:
        self._id = id
        self._user_id = user_id
        self._content = content
        self._sent_at = sent_at

    @property
    @override
    def id(self) -> MessageId:
        return self._id

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def content(self) -> str:
        return self._content

    @property
    def sent_at(self) -> datetime.datetime:
        return self._sent_at


class UserMessage(Message):
    pass


class BotMessage(Message):
    pass


class MessageRepository(abc.ABC):
    @abc.abstractmethod
    async def get(self, id: MessageId) -> Message | None:
        pass

    @abc.abstractmethod
    def add(self, message: Message) -> None:
        pass

    @abc.abstractmethod
    async def get_user_messages(self, user_id: UserId) -> Sequence[Message]:
        pass
