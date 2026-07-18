import asyncio
import re

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_i18n import I18nContext
from dishka import FromDishka

from app.bot.utils.admin_notify import notify_admins_group
from app.bot.utils.get_engine_emoji import get_engine_emoji
from app.bot.utils.save_track import save_track_with_source
from app.config.settings import settings
from app.database.models.download_context import DownloadContext, EntityType, DownloadMode
from app.database.repositories import TrackRepository
from app.modules.musicocean.enums import Engine
from app.modules.musicocean_tg import TelegramMusicOceanClient
from app.modules.musicocean_tg.utils import prefix_to_engine

from app.config.log import get_logger

logger = get_logger(__name__)

router = Router()


async def answer_audio_retrying(message: Message, file_id: str, attempts: int = 3):
    for attempt in range(attempts):
        try:
            return await message.answer_audio(audio=file_id)
        except TelegramNetworkError:
            if attempt == attempts - 1:
                raise
            await asyncio.sleep(3 * (attempt + 1))


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
    # anonymous senders (posting as a channel) have no from_user; use the
    # sender channel as a fallback so downloads still attribute to someone
    sender = message.from_user or message.sender_chat

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

    entity_kind = EntityType.ALBUM if entity_type == "al" else EntityType.PLAYLIST

    match entity_type:
        case "al":
            group_tracks = True  # todo!! maybe..
            album = await musicocean.get_album(engine, entity_id)
            tracks = await musicocean.get_album_tracks(engine, entity_id)
            group_artist, group_title = album.artist_name, album.title
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
            group_artist, group_title = "", playlist.title
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

    # notify admins once about the group, not about each track
    await notify_admins_group(
        message.bot, settings.telegram.admins,
        engine, group_artist, group_title,
        entity_id, sender
    )

    failed = 0
    async for track in musicocean.download_tracks(
            engine,
            tracks,
            track_repo
    ):
        # one bad track (stale file_id, network hiccup) must not kill the batch
        try:
            try:
                sent = await answer_audio_retrying(message, track.file_id)
            except TelegramBadRequest:
                # cached file_id went stale (e.g. legacy worker upload) — re-fetch
                # fresh through a worker (not the main bot) and refresh the cached row
                fresh = await musicocean.redownload_track(engine, track.track_id)
                sent = await answer_audio_retrying(message, fresh.file_id)
                await track_repo.update_file(
                    track.track_id, engine,
                    sent.audio.file_id, sent.audio.file_unique_id
                )

            # todo move db-saving logic to one place (handlers or tg_musicocean)
            await save_track_with_source(
                track_repo,
                engine=engine,
                track_id=track.track_id,
                cached=track,
                file_id=sent.audio.file_id,
                file_unique_id=sent.audio.file_unique_id,
                user_id=sender.id,
                download_context=DownloadContext.ENTITY,
                entity_type=entity_kind,
                download_mode=DownloadMode.MULTI
            )
        except Exception as e:
            failed += 1
            logger.warning(f"skipping track {track.track_id} in batch: {e}")

    done_text = i18n.get('downloaded')
    if failed:
        done_text += f" ({failed} failed)"
    await message.answer(done_text)
