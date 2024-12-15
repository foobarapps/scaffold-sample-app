import dataclasses
import datetime


@dataclasses.dataclass(frozen=True)
class Message:
    content: str
    sent_at: datetime.datetime
    is_from_bot: bool
