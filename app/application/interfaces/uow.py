import abc
from types import TracebackType

from app.domain.message import MessageRepository


class UnitOfWork(abc.ABC):
    messages: MessageRepository

    @abc.abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def __aenter__(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def __aexit__(self, exc_type: type, exc: BaseException, tb: TracebackType) -> None:
        raise NotImplementedError


class UnitOfWorkFactory(abc.ABC):
    @abc.abstractmethod
    def create(self) -> UnitOfWork:
        pass
