from aiogram import Bot
from aiogram.types import User

from app.bot.utils.get_engine_emoji import get_engine_emoji
from app.config.log import get_logger
from app.modules.musicocean.enums import Engine

logger = get_logger(__name__)

ENGINE_NAMES = {
    Engine.DEEZER: "Deezer",
    Engine.SOUNDCLOUD: "SoundCloud",
    Engine.YOUTUBE: "YouTube",
    Engine.SPOTIFY: "Spotify",
    Engine.YANDEX: "Yandex Music",
}


def _format_user(user: User) -> str:
    if user.username:
        return "@" + user.username
    last = f" {user.last_name}" if user.last_name else ""
    return f"<a href='tg://user?id={user.id}'>{user.first_name}{last}</a>"


def _format(engine: Engine, artist_name: str, title: str, entity_id: int | str, user: User) -> str:
    name = f"{artist_name} - {title}" if artist_name else title
    return (
        f"<blockquote><b><i>{name}</i></b></blockquote>\n\n"
        f"• <b>Engine</b>: {get_engine_emoji(engine)}  <code>{ENGINE_NAMES[engine]}</code>\n"
        f"• <b>Track ID</b>: <code>{entity_id}</code>\n"
        f"• <b>Downloaded by</b>: {_format_user(user)}"
    )


async def _broadcast(bot: Bot, admins: list[int], text: str) -> None:
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, text)
        except Exception as e:
            logger.warning(f"admin notify failed #{admin_id}: {e}")


async def notify_admins_track(
        bot: Bot,
        admins: list[int],
        engine: Engine,
        artist_name: str,
        title: str,
        track_id: int | str,
        user: User
) -> None:
    await _broadcast(bot, admins, _format(engine, artist_name, title, track_id, user))


async def notify_admins_group(
        bot: Bot,
        admins: list[int],
        engine: Engine,
        artist_name: str,
        title: str,
        entity_id: int | str,
        user: User
) -> None:
    # one notification for the whole album/playlist, same track-info format
    await _broadcast(bot, admins, _format(engine, artist_name, title, entity_id, user))
