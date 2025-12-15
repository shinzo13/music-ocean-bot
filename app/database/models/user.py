from typing import List, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Boolean, BigInteger, JSON, TypeDecorator
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.pydantic_model import PydanticModel
from app.database.models.base import Base, TimestampMixin, IntIDMixin
from app.modules.musicocean.enums.engine import Engine

if TYPE_CHECKING:
    from app.database.models import Track


class UserSettings(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    selected_engine: Engine = Engine.DEEZER
    track_preview_covers: bool = True

class User(Base, TimestampMixin, IntIDMixin):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)

    settings: Mapped[UserSettings] = mapped_column(
        PydanticModel(UserSettings),
        nullable=False,
        default=UserSettings().model_dump(mode="json")
    )

    downloaded_tracks: Mapped[List["Track"]] = relationship(back_populates="downloaded_by")