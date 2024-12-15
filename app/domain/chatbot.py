import abc
from collections.abc import Sequence

from .message import BotMessage, Message


class Chatbot(abc.ABC):
    @abc.abstractmethod
    def reply_to_conversation(self, conversation: Sequence[Message]) -> BotMessage:
        pass
