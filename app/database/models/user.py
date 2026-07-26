from typing import List, TYPE_CHECKING, Optional

from pydantic import BaseModel
from sqlalchemy import Boolean, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base, TimestampMixin, IntIDMixin
from app.database.models.pydantic_model import PydanticModel
from app.modules.musicocean.enums.engine import Engine

if TYPE_CHECKING:
    from app.database.models import BaseTrack


class LastfmSettings(BaseModel):
    enabled: bool = False
    username: Optional[str] = None


class UserSettings(BaseModel):
    locale: Optional[str] = None
    selected_engine: Engine = Engine.DEEZER
    track_preview_covers: bool = True
    # admins opt in to download notifications; off by default for new admins
    admin_download_notifications: bool = False

    lastfm: LastfmSettings = LastfmSettings()


class User(Base, TimestampMixin, IntIDMixin):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    username: Mapped[str | None] = mapped_column(String, nullable=True)
    is_dm: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)

    settings: Mapped[UserSettings] = mapped_column(
        PydanticModel(UserSettings),
        nullable=False,
        default=UserSettings().model_dump(mode="json")
    )

    downloaded_tracks: Mapped[List["BaseTrack"]] = relationship(back_populates="downloaded_by")
