import datetime
from collections.abc import Sequence
from typing import override

from openai import AsyncOpenAI
from scaffold.uuid7 import uuid7

from app.domain.chatbot import Chatbot
from app.domain.message import BotMessage, Message, MessageId, UserMessage


class Echobot(Chatbot):
    @override
    async def reply_to_conversation(self, conversation: Sequence[Message]) -> BotMessage:
        latest_message = conversation[0]
        return BotMessage(
            id=MessageId(uuid7()),
            user_id=latest_message.user_id,
            content=latest_message.content,
            sent_at=datetime.datetime.now(),
        )


class OpenAIBot(Chatbot):
    def __init__(self, client: AsyncOpenAI) -> None:
        self.client = client

    @override
    async def reply_to_conversation(self, conversation: Sequence[Message]) -> BotMessage:
        latest_message = conversation[0]

        completion = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user" if isinstance(m, UserMessage) else "assistant", "content": m.content}  # type: ignore[misc]
                for m in reversed(conversation)
            ],
        )

        return BotMessage(
            id=MessageId(uuid7()),
            user_id=latest_message.user_id,
            content=completion.choices[0].message.content or "",
            sent_at=datetime.datetime.now(),
        )
