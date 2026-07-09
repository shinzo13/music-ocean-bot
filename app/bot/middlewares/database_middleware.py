from typing import Callable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.enums import ChatType
from aiogram.types import Message, User as TelegramUser, Update, InputTextMessageContent
from aiogram_i18n.types import InlineQueryResultArticle
from typing_extensions import Awaitable

from app.config.log import get_logger
from app.database.models import User as DatabaseUser
from app.database.repositories import UserRepository

logger = get_logger(__name__)


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        user_repo: UserRepository = await data["dishka_container"].get(UserRepository)
        tg_user: TelegramUser | None = data.get("event_from_user")

        # anonymous senders (posting as a channel in discussion comments) arrive
        # with no from_user; fall back to the sender channel id so the flow keeps
        # working instead of crashing handlers that require a user object
        sender_chat = event.message.sender_chat if event.message else None
        if tg_user is not None:
            user_id = tg_user.id
            language_code = tg_user.language_code
        elif sender_chat is not None:
            user_id = sender_chat.id
            language_code = None
        else:
            return await handler(event, data)

        db_user: DatabaseUser = await user_repo.get_user_by_id(user_id) \
                                or await user_repo.add_user(user_id=user_id)

        if not db_user.settings.locale and language_code:
            logger.debug(f"set lang: {language_code}")
            await user_repo.update_user_settings(
                db_user.user_id,
                locale=language_code
            )

        if db_user.is_banned:
            if event.message:
                emoji = '<tg-emoji emoji-id="5346155619663491339">🎧</tg-emoji>'
                await event.message.answer(f'you are banned{emoji}{emoji}')
            elif event.callback_query:
                await event.callback_query.answer(f'you are banned!!!!')
            elif event.inline_query:
                await event.inline_query.answer([InlineQueryResultArticle(
                    id='banned',
                    title='you are banned!!!',
                    description=f'🗣🗣',
                    input_message_content=InputTextMessageContent(
                        message_text="im banned🗣🗣🗣🗣"
                    )
                )], cache_time=0, is_personal=True)
            return None

        # is_dm should flip to True only when the user actually DMs the bot,
        # not on any interaction (inline queries, group messages, callbacks)
        if not db_user.is_dm and event.message and event.message.chat.type == ChatType.PRIVATE:
            await user_repo.update_user(db_user.user_id, is_dm=True)

        data["user"] = db_user

        return await handler(event, data)
