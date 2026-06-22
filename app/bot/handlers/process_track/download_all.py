import re

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_i18n import I18nContext
from dishka import FromDishka

from app.bot.utils.get_engine_emoji import get_engine_emoji
from app.database.repositories import TrackRepository
from app.modules.musicocean.enums import Engine
from app.modules.musicocean_tg import TelegramMusicOceanClient
from app.modules.musicocean_tg.utils import prefix_to_engine

router = Router()


@router.message(
    CommandStart(
        deep_link=True,
        magic=F.args.regexp(r'^(dz|sc|yt|sp)_(al|pl|ar)_([\w-]+)$').as_("deeplink_match")
    )
)
async def handle_deeplink(
        message: Message,
        deeplink_match: re.Match,
        musicocean: FromDishka[TelegramMusicOceanClient],
        track_repo: FromDishka[TrackRepository],
        i18n: I18nContext,
):
    engine_prefix = deeplink_match.group(1)
    entity_type = deeplink_match.group(2)
    entity_id = deeplink_match.group(3)

    try:
        engine = prefix_to_engine(engine_prefix)
    except ValueError:
        await message.answer("invalid link")
        return

    if engine in (Engine.DEEZER, Engine.SOUNDCLOUD):
        entity_id = int(entity_id)

    engine_emoji = get_engine_emoji(engine)

    match entity_type:
        case "al":
            group_tracks = True  # todo!! maybe..
            album = await musicocean.get_album(engine, entity_id)
            tracks = await musicocean.get_album_tracks(engine, entity_id)
            text = i18n.get(
                'entity-album',
                title=album.title,
                artist_name=album.artist_name,
                cover_url=album.cover_url
            )
        case "pl":
            group_tracks = False
            playlist = await musicocean.get_playlist(engine, entity_id)
            tracks = await musicocean.get_playlist_tracks(engine, entity_id)
            text = i18n.get(
                'entity-playlist',
                title=playlist.title,
                artist_name=playlist.track_count,
                cover_url=playlist.cover_url
            )
        # here was artist but nah i wont download all the artists tracks
        case _:
            await message.answer(i18n.get('invalid-link'))
            return

    await message.answer(text)
    await message.answer(i18n.get('downloading'))

    async for track in musicocean.download_tracks(
            engine,
            tracks,
            track_repo
    ):
        try:
            sent = await message.answer_audio(audio=track.file_id)
        except TelegramBadRequest:
            # cached file_id went stale (e.g. legacy worker upload) — re-fetch
            # fresh via the main bot and refresh the cached row
            fresh = await musicocean.download_track(engine, track.track_id)
            sent = await message.answer_audio(audio=fresh.file_id)
            await track_repo.update_file(
                track.track_id, engine,
                sent.audio.file_id, sent.audio.file_unique_id
            )

        # todo move db-saving logic to one place (handlers or tg_musicocean)
        if not await track_repo.get_track(track.track_id, engine):
            await track_repo.add_track(
                engine=engine,
                track_id=track.track_id,
                telegram_file_id=sent.audio.file_id,
                telegram_file_unique_id=sent.audio.file_unique_id,
                user_id=message.from_user.id,
            )

    await message.answer(i18n.get('downloaded'))
