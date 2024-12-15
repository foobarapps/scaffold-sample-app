from app.application.dtos.message import Message as MessageDTO
from app.domain.message import BotMessage, Message


class MessageAssembler:
    @staticmethod
    def assemble_dto(message: Message) -> MessageDTO:
        return MessageDTO(
            content=message.content,
            sent_at=message.sent_at,
            is_from_bot=isinstance(message, BotMessage),
        )
