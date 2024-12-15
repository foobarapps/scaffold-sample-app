from typing import override

from app.application.services.message_service import MessageService

from ..tasks.reply_to_conversation_task import ReplyToConversationTask
from .base import BaseTaskHandler


class ReplyToConversationTaskHandler(BaseTaskHandler[ReplyToConversationTask]):
    def __init__(
        self,
        message_service: MessageService,
    ) -> None:
        self.message_service = message_service

    @override
    async def handle(self, task: ReplyToConversationTask) -> None:
        await self.message_service.reply_to_user_latest_message(task.user_id)
