from sqlalchemy import BigInteger, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base_track import BaseTrack
from app.modules.musicocean.enums import Engine


class SoundCloudTrack(BaseTrack):
    __tablename__ = "soundcloud_tracks"

    id: Mapped[int] = mapped_column(ForeignKey("base_tracks.id"), primary_key=True)
    track_id: Mapped[int] = mapped_column(BigInteger)

    __mapper_args__ = {"polymorphic_identity": Engine.SOUNDCLOUD}