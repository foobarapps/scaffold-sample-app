import dataclasses
import uuid

from app.application.interfaces.task_queue import Task


@dataclasses.dataclass(frozen=True)
class ReplyToConversationTask(Task):
    user_id: uuid.UUID
