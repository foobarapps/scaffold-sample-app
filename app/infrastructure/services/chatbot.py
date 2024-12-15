import datetime
from collections.abc import Sequence
from typing import override

from scaffold.uuid7 import uuid7

from app.domain.chatbot import Chatbot
from app.domain.message import BotMessage, Message, MessageId


class Echobot(Chatbot):
    @override
    def reply_to_conversation(self, conversation: Sequence[Message]) -> BotMessage:
        latest_message = conversation[0]
        return BotMessage(
            id=MessageId(uuid7()),
            user_id=latest_message.user_id,
            content=latest_message.content,
            sent_at=datetime.datetime.now(),
        )
