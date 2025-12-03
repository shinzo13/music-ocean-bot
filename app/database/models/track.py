from sqlalchemy import String, ForeignKey, Enum, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.models.base import Base, TimestampMixin, IntIDMixin
from app.modules.musicocean.enums.engine import Engine


class Track(Base, TimestampMixin, IntIDMixin):
    __tablename__ = "tracks"

    engine: Mapped[Engine] = mapped_column(Enum(Engine, name="engine_enum"))
    track_id: Mapped[int] = mapped_column(BigInteger)
    telegram_file_id: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))

    downloaded_by: Mapped["User"] = relationship(back_populates="downloaded_tracks") # noqa