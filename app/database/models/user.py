from sqlalchemy import Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.models.base import Base, TimestampMixin, IntIDMixin


class User(Base, TimestampMixin, IntIDMixin):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer)
    is_admin: Mapped[bool] = mapped_column(Boolean)
    is_banned: Mapped[bool] = mapped_column(Boolean)
    downloaded: Mapped["Track"] = relationship(back_populates="users") # noqa