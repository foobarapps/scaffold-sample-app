from collections.abc import Sequence
from typing import override

import sqlalchemy as sa
from scaffold.persistence.repository import GenericSqlRepository

from app.domain.message import (
    BotMessage,
    Message,
    MessageId,
    MessageRepository,
    UserId,
    UserMessage,
)
from app.infrastructure.persistence_model import Message as MessageDTO


class SqlMessageRepository(GenericSqlRepository[Message, MessageId, MessageDTO], MessageRepository):
    @override
    async def get_user_messages(self, user_id: UserId) -> Sequence[Message]:
        dtos = (
            await self._session.scalars(
                sa.select(MessageDTO).where(MessageDTO.user_id == user_id.value).order_by(MessageDTO.sent_at.desc()),
            )
        ).all()
        return [self.map_dto_to_entity_and_track(dto) for dto in dtos]

    @override
    def _map_entity_to_dto(self, entity: Message) -> MessageDTO:
        return MessageDTO(
            id=entity.id.value,
            user_id=entity.user_id.value,
            content=entity.content,
            sent_at=entity.sent_at,
            is_from_bot=isinstance(entity, BotMessage),
        )

    @override
    def _map_dto_to_entity(self, dto: MessageDTO) -> Message:
        if dto.is_from_bot:
            return BotMessage(
                id=MessageId(dto.id),
                user_id=UserId(dto.user_id),
                content=dto.content,
                sent_at=dto.sent_at,
            )
        return UserMessage(
            id=MessageId(dto.id),
            user_id=UserId(dto.user_id),
            content=dto.content,
            sent_at=dto.sent_at,
        )
