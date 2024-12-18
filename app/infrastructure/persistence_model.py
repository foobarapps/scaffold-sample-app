import datetime
import uuid

from scaffold.persistence.model import Base, EntityMixin, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column


class Message(EntityMixin, TimestampMixin, Base):
    __tablename__ = "message"

    user_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    content: Mapped[str]
    sent_at: Mapped[datetime.datetime] = mapped_column(nullable=False)
    is_from_bot: Mapped[bool] = mapped_column(nullable=False)
