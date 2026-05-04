import re

from aiogram import Router, F, Bot
from aiogram.types import InlineQuery
from dishka import FromDishka

from app.bot.utils.search_results import (
    get_album_results,
    get_artist_results,
    get_playlist_results,
    usage_guide_result, get_track_results, not_supported_result
)
from app.config.log import get_logger
from app.database.models import User as DatabaseUser
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean_tg import TelegramMusicOceanClient
from app.modules.musicocean_tg.utils import prefix_to_engine

logger = get_logger(__name__)

router = Router()

DEEZER_REGEX = re.compile(r"https?://(?:www\.)?deezer\.com/\w+/(track|album|playlist|artist)/(\d+)")
SPOTIFY_REGEX = re.compile(r"https?://open\.spotify\.com/(track|album|playlist|artist)/([A-Za-z0-9]+)")
SOUNDCLOUD_REGEX = re.compile(r"https?://(?:www\.)?soundcloud\.com/[\w-]+/[\w-]+")
YOUTUBE_REGEX = re.compile(r"https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+)")

@router.inline_query(
    F.query.regexp(DEEZER_REGEX).as_('match') | \
    F.query.regexp(SPOTIFY_REGEX).as_('match')
)
async def inline_query(
        query: InlineQuery,
        match: re.Match,
        user: DatabaseUser,
        musicocean: FromDishka[TelegramMusicOceanClient]
):
    engine = Engine.DEEZER if 'deezer' in query.query else Engine.SPOTIFY
    logger.info(f"User #{query.from_user.id} searched {engine} link: \"{query.query}\"")
    entity_type, entity_id = match.groups()
    if engine == Engine.DEEZER:
        entity_id = int(entity_id)


    match entity_type:
        case "track":
            tracks = [await musicocean.get_track(engine, entity_id)]
        case "album":
            tracks = await musicocean.get_album_tracks(engine, entity_id)
        case "artist":
            tracks = await musicocean.get_artist_tracks(engine, entity_id)
        case "playlist":
            tracks = await musicocean.get_playlist_tracks(engine, entity_id)
        case "" | _:
            return

    await query.answer(
        await get_track_results(
            engine,
            tracks,
            user.settings.track_preview_covers
        ),
        cache_time=0
    )

@router.inline_query(F.query.regexp(YOUTUBE_REGEX).as_('match'))
async def inline_query(
        query: InlineQuery,
        match: re.Match,
        user: DatabaseUser,
        musicocean: FromDishka[TelegramMusicOceanClient]
):
    track_id = match.group(1)
    track = await musicocean.get_track(Engine.YOUTUBE, track_id)
    await query.answer(
        await get_track_results(
            Engine.YOUTUBE,
            [track],
            user.settings.track_preview_covers
        ),
        cache_time=0
    )

@router.inline_query(F.query.regexp(SOUNDCLOUD_REGEX))
async def inline_query(query: InlineQuery):
    await query.answer(not_supported_result("SoundCloud link search"))