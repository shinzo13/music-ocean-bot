from aiogram import Bot

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


def _format(header: str, engine: Engine, artist_name: str, title: str) -> str:
    name = f"{artist_name} - {title}" if artist_name else title
    return (
        f"{header}\n\n"
        f"<blockquote><b><i>{name}</i></b></blockquote>\n\n"
        f"• <b>Engine</b>: {get_engine_emoji(engine)}  <code>{ENGINE_NAMES[engine]}</code>"
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
        title: str
) -> None:
    await _broadcast(bot, admins, _format("⬇️ <b>New download</b>", engine, artist_name, title))


async def notify_admins_group(
        bot: Bot,
        admins: list[int],
        engine: Engine,
        kind: str,
        artist_name: str,
        title: str
) -> None:
    # kind: "album" | "playlist" — notify once about the group, not each track
    await _broadcast(bot, admins, _format(f"⬇️ <b>New {kind} download</b>", engine, artist_name, title))
