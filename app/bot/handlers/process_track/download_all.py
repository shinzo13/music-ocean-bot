from aiogram import Router, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message
import re

from dishka import FromDishka

from app.bot.utils.get_engine_emoji import get_engine_emoji
from app.modules.musicocean_tg import TelegramMusicOceanClient
from app.modules.musicocean_tg.utils import prefix_to_engine

router = Router()


@router.message(
    CommandStart(
        deep_link=True,
        magic=F.args.regexp(r'^(dz|sc|yt|sp)_(al|pl|ar)_(\d+)$').as_("deeplink_match")
    )
)
async def handle_deeplink(
        message: Message,
        deeplink_match: re.Match,
        musicocean: FromDishka[TelegramMusicOceanClient],
):
    engine_prefix = deeplink_match.group(1)
    entity_type = deeplink_match.group(2)
    entity_id = int(deeplink_match.group(3))

    try:
        engine = prefix_to_engine(engine_prefix)
    except ValueError:
        await message.answer("invalid link")
        return

    engine_emoji = get_engine_emoji(engine)

    match entity_type:
        case "al":
            group_tracks = True
            album = await musicocean.get_album(engine, entity_id)
            tracks = await musicocean.get_album_tracks(engine, entity_id)
            text = f'<b>{engine_emoji}{album.title}</b>\n<i>{album.artist_name}</i><a href="{album.cover_url}">︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎</a>'
        case "pl":
            group_tracks = False
            playlist = await musicocean.get_playlist(engine, entity_id)
            tracks = await musicocean.get_playlist_tracks(engine, entity_id)
            text = f'<b>{engine_emoji}{playlist.title}</b>\n<i>{playlist.track_count} tracks</i><a href="{playlist.cover_url}">︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎︎</a>'
        # here was artist but nah i wont download all the artists tracks
        case _:
            await message.answer("invalid link")
            return

    await message.answer(text)
    await message.answer("downloading..")
    await message.answer("okay actually no")





