from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base, TimestampMixin, IntIDMixin
from app.database.models.download_context import DownloadContext, EntityType, DownloadMode
from app.modules.musicocean.enums.engine import Engine


class BaseTrack(Base, TimestampMixin, IntIDMixin):
    __tablename__ = "base_tracks"

    engine: Mapped[Engine] = mapped_column(Enum(Engine, name="engine_enum"))
    telegram_file_id: Mapped[str] = mapped_column(String)
    telegram_file_unique_id: Mapped[str | None] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    download_context: Mapped[DownloadContext] = mapped_column(
        Enum(DownloadContext, name="download_context_enum"),
        default=DownloadContext.SEARCH,
        server_default=DownloadContext.SEARCH.value
    )
    entity_type: Mapped[EntityType | None] = mapped_column(
        Enum(EntityType, name="entity_type_enum"), nullable=True
    )
    download_mode: Mapped[DownloadMode | None] = mapped_column(
        Enum(DownloadMode, name="download_mode_enum"), nullable=True
    )

    downloaded_by: Mapped["User"] = relationship(back_populates="downloaded_tracks")  # noqa

    __mapper_args__ = {
        "polymorphic_on": "engine",
        "polymorphic_identity": None,
    }
