import re

from aiogram import Router, F
from aiogram.types import InlineQuery
from aiogram_i18n import I18nContext
from dishka import FromDishka

from app.bot.utils.search_results import (
    get_track_results, not_supported_result
)
from app.config.log import get_logger
from app.database.models import User as DatabaseUser
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean_tg import TelegramMusicOceanClient

logger = get_logger(__name__)

router = Router()

DEEZER_REGEX = re.compile(r"https?://(?:www\.)?deezer\.com/(?:\w+/)?(track|album|playlist|artist)/(\d+)")
SPOTIFY_REGEX = re.compile(r"https?://open\.spotify\.com/(track|album|playlist|artist)/([A-Za-z0-9]+)")
SOUNDCLOUD_REGEX = re.compile(r"https?://(?:www\.)?soundcloud\.com/[\w-]+/[\w-]+")
YOUTUBE_REGEX = re.compile(r"https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+)")

YANDEX_DOMAIN = r"https?://(?:www\.)?music\.yandex\.(?:ru|com|by|kz|uz)"
YANDEX_REGEX = re.compile(YANDEX_DOMAIN + r"/")
YANDEX_TRACK_REGEX = re.compile(YANDEX_DOMAIN + r"/album/\d+/track/(\d+)")
YANDEX_ALBUM_REGEX = re.compile(YANDEX_DOMAIN + r"/album/(\d+)")
YANDEX_ARTIST_REGEX = re.compile(YANDEX_DOMAIN + r"/artist/(\d+)")
YANDEX_PLAYLIST_REGEX = re.compile(YANDEX_DOMAIN + r"/users/([\w.-]+)/playlists/(\d+)")


@router.inline_query(
    F.query.regexp(DEEZER_REGEX).as_('match') | \
    F.query.regexp(SPOTIFY_REGEX).as_('match')
)
async def inline_query(
        query: InlineQuery,
        match: re.Match,
        user: DatabaseUser,
        i18n: I18nContext,
        musicocean: FromDishka[TelegramMusicOceanClient]
):
    engine = Engine.DEEZER if 'deezer' in query.query else Engine.SPOTIFY
    logger.info(f"User #{query.from_user.id} searched {engine} link: \"{query.query}\"")
    entity_type, entity_id = match.groups()
    if engine == Engine.DEEZER:
        entity_id = int(entity_id)

    # Spotify returns 403 on playlist tracks and artist top-tracks for
    # client-credentials apps since its 2024 API restrictions.
    if engine == Engine.SPOTIFY and entity_type in ("playlist", "artist"):
        await query.answer(
            not_supported_result(i18n.get('feature-spotify-link-search')),
            cache_time=0
        )
        return

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


@router.inline_query(F.query.regexp(YANDEX_REGEX))
async def inline_query(
        query: InlineQuery,
        user: DatabaseUser,
        musicocean: FromDishka[TelegramMusicOceanClient]
):
    logger.info(f"User #{query.from_user.id} searched Yandex link: \"{query.query}\"")
    text = query.query

    if m := YANDEX_TRACK_REGEX.search(text):
        tracks = [await musicocean.get_track(Engine.YANDEX, m.group(1))]
    elif m := YANDEX_ALBUM_REGEX.search(text):
        tracks = await musicocean.get_album_tracks(Engine.YANDEX, m.group(1))
    elif m := YANDEX_ARTIST_REGEX.search(text):
        tracks = await musicocean.get_artist_tracks(Engine.YANDEX, m.group(1))
    elif m := YANDEX_PLAYLIST_REGEX.search(text):
        playlist_id = f"{m.group(1)}:{m.group(2)}"
        tracks = await musicocean.get_playlist_tracks(Engine.YANDEX, playlist_id)
    else:
        return

    await query.answer(
        await get_track_results(
            Engine.YANDEX,
            tracks,
            user.settings.track_preview_covers
        ),
        cache_time=0
    )


@router.inline_query(F.query.regexp(SOUNDCLOUD_REGEX))
async def inline_query(query: InlineQuery, i18n: I18nContext):
    await query.answer(not_supported_result(i18n.get('feature-soundcloud-link-search')))
