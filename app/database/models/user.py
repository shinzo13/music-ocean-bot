from typing import List, TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Boolean, BigInteger, JSON, TypeDecorator
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.pydantic_model import PydanticModel
from app.database.models.base import Base, TimestampMixin, IntIDMixin
from app.modules.musicocean.enums.engine import Engine

if TYPE_CHECKING:
    from app.database.models import BaseTrack


class SpotifySettings(BaseModel):
    enabled: bool = False
    connection_code: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None

class UserSettings(BaseModel):

    selected_engine: Engine = Engine.DEEZER
    track_preview_covers: bool = True

    spotify: Mapped[SpotifySettings] = mapped_column(
        PydanticModel(SpotifySettings),
        nullable=False,
        default=SpotifySettings().model_dump(mode="json")
    )

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

    downloaded_tracks: Mapped[List["BaseTrack"]] = relationship(back_populates="downloaded_by")