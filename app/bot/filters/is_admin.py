from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject

from app.database.models import User


class IsAdmin(BaseFilter):
    async def __call__(self, event: TelegramObject, user: User | None = None) -> bool:
        return bool(user and user.is_admin)
