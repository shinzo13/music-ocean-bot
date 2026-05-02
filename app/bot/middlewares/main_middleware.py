from typing import Callable, Dict, Any, Optional

from aiogram import BaseMiddleware
from aiogram.types import Message, User as TelegramUser
from typing_extensions import Awaitable

from app.config.log import get_logger
from app.database.models import User as DatabaseUser
from app.database.repositories import UserRepository

logger = get_logger(__name__)


class MainMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user_repo = await data["dishka_container"].get(UserRepository)
        tg_user: TelegramUser | None = data.get("event_from_user")

        if tg_user is None:
            return await handler(event, data)

        db_user: DatabaseUser =  await user_repo.get_user_by_id(tg_user.id) \
                                 or await user_repo.add_user(user_id=tg_user.id)

        if db_user.is_banned:
            return None

        if not db_user.is_dm:
            await user_repo.update_user(db_user.user_id, is_dm=True)

        data["user"] = db_user

        return await handler(event, data)
