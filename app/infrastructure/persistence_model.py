import datetime
import uuid

import sqlalchemy as sa
from scaffold.persistence.model import Base, EntityMixin, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column


class User(EntityMixin, TimestampMixin, Base):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)


class Message(EntityMixin, TimestampMixin, Base):
    __tablename__ = "message"

    user_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey("user.id"),
        nullable=False,
    )
    content: Mapped[str]
    sent_at: Mapped[datetime.datetime] = mapped_column(nullable=False)
    is_from_bot: Mapped[bool] = mapped_column(nullable=False)
