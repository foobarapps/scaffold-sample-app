import dataclasses
import datetime
import uuid
from collections.abc import AsyncGenerator, Sequence

from app.application.assemblers.message_assembler import MessageAssembler
from app.application.backgroundtasks.tasks.reply_to_conversation_task import (
    ReplyToConversationTask,
)
from app.application.dtos.message import Message as MessageDTO
from app.application.interfaces.pub_sub_service import PubSubService
from app.application.interfaces.task_queue import TaskQueue
from app.application.interfaces.uow import UnitOfWorkFactory
from app.domain.chatbot import Chatbot
from app.domain.message import MessageId, UserId, UserMessage


@dataclasses.dataclass
class MessageDoesNotExistError(Exception):
    message_id: str


class MessageService:
    def __init__(
        self,
        unit_of_work_factory: UnitOfWorkFactory,
        chatbot: Chatbot,
        task_queue: TaskQueue,
        pub_sub: PubSubService,
    ) -> None:
        self.unit_of_work_factory = unit_of_work_factory
        self.chatbot = chatbot
        self.task_queue = task_queue
        self.pub_sub = pub_sub

    async def get_messages_for_conversation(self, user_id: uuid.UUID) -> Sequence[MessageDTO]:
        uow = self.unit_of_work_factory.create()
        async with uow:
            messages = await uow.messages.get_user_messages(UserId(user_id))
            return [MessageAssembler().assemble_dto(message) for message in messages]

    async def send_user_message(
        self,
        user_id: uuid.UUID,
        message_id: uuid.UUID,
        content: str,
        sent_at: datetime.datetime,
    ) -> None:
        uow = self.unit_of_work_factory.create()
        async with uow:
            message = UserMessage(
                id=MessageId(message_id),
                user_id=UserId(user_id),
                content=content,
                sent_at=sent_at,
            )
            uow.messages.add(message)
            await uow.commit()

            await self.task_queue.enqueue(ReplyToConversationTask(user_id))

            await self.pub_sub.publish(self.get_channel_name(user_id), str(message_id))

    async def reply_to_user_latest_message(self, user_id: uuid.UUID) -> None:
        uow = self.unit_of_work_factory.create()
        async with uow:
            messages = await uow.messages.get_user_messages(UserId(user_id))

            reply = await self.chatbot.reply_to_conversation(messages)

            uow.messages.add(reply)
            await uow.commit()

            await self.pub_sub.publish(self.get_channel_name(user_id), str(reply.id.value))

    async def subscribe_to_user_messages(self, user_id: uuid.UUID) -> AsyncGenerator[MessageDTO]:
        uow = self.unit_of_work_factory.create()
        async for message_id_str in self.pub_sub.subscribe(self.get_channel_name(user_id)):
            async with uow:
                message = await uow.messages.get(MessageId(uuid.UUID(message_id_str)))

                if not message:
                    raise MessageDoesNotExistError(message_id_str)

                message_dto = MessageAssembler().assemble_dto(message)

                yield message_dto

    @staticmethod
    def get_channel_name(user_id: uuid.UUID) -> str:
        return f"user:{user_id}:messages"
