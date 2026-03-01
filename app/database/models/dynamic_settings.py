from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base, TimestampMixin, IntIDMixin


class DynamicSettings(Base, TimestampMixin, IntIDMixin):
    __tablename__ = "dynamic_settings"

    bot_username: Mapped[str] = mapped_column(nullable=True)