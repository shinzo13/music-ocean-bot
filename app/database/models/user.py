from typing import List

from sqlalchemy import Boolean, Enum, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base, TimestampMixin, IntIDMixin
from app.modules.musicocean.enums.engine import Engine


class User(Base, TimestampMixin, IntIDMixin):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    selected_engine: Mapped[Engine] = mapped_column(Enum(Engine, name="engine_enum"))

    downloaded_tracks: Mapped[List["Track"]] = relationship(back_populates="downloaded_by")  # noqa
