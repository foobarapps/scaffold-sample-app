import typing

from scaffold.persistence import GenericSqlUnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.uow import UnitOfWork, UnitOfWorkFactory
from app.infrastructure.repositories.sql_message_repository import SqlMessageRepository


class SqlUnitOfWork(GenericSqlUnitOfWork, UnitOfWork):
    @typing.override
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

        self.messages = SqlMessageRepository(session)


class SqlUnitOfWorkFactory(UnitOfWorkFactory):
    def __init__(self, session_factory: typing.Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory

    @typing.override
    def create(self) -> SqlUnitOfWork:
        return SqlUnitOfWork(self._session_factory())
