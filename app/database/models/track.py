from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.models.base import Base, TimestampMixin, IntIDMixin


class Track(Base, TimestampMixin, IntIDMixin):
    __tablename__ = "tracks"

    engine: Mapped[str] = mapped_column(String)
    track_id: Mapped[int] = mapped_column(Integer)
    telegram_file_id: Mapped[int] = mapped_column(Integer)
    downloaded_by: Mapped["User"] = relationship(back_populates="tracks") # noqa
