import asyncio
from typing import Awaitable, Callable

from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, BufferedInputFile, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dishka import FromDishka

from app.bot.callbacks.admin_panel_callback import AdminPanelCallback, AdminPanelPath
from app.bot.utils.stats_banner import render_engine_banner, render_context_banner, render_speed_banner
from app.database.models.download_context import EntityType, DownloadMode
from app.database.repositories import TrackRepository

router = Router()


class StatsPageCallback(CallbackData, prefix="astats"):
    page: str


ENTITY_LABELS = {
    EntityType.ALBUM: "album",
    EntityType.PLAYLIST: "playlist",
    EntityType.ARTIST: "artist",
}

MODE_LABELS = {
    DownloadMode.SINGLE: "single",
    DownloadMode.MULTI: "multi",
}


def _engine_banner(stats: dict) -> bytes:
    return render_engine_banner({e.value.lower(): c for e, c in stats['by_engine'].items()})


def _context_banner(stats: dict) -> bytes:
    return render_context_banner({c.value.lower(): n for c, n in stats['by_context'].items()})


def _speed_banner(stats: dict) -> bytes:
    return render_speed_banner(
        {e.value.lower(): v for e, v in stats['speed_by_engine'].items()}
    )


# page key -> (switch-button label, banner renderer); add new pages here
PAGES: dict[str, tuple[str, Callable[[dict], bytes]]] = {
    "engine": ("📀 by engine", _engine_banner),
    "context": ("🔀 by context", _context_banner),
    "speed": ("⚡ avg speed", _speed_banner),
}

DEFAULT_PAGE = "engine"


def page_keyboard(current: str):
    kb = InlineKeyboardBuilder()
    for key, (label, _) in PAGES.items():
        if key != current:
            kb.button(text=label, callback_data=StatsPageCallback(page=key).pack())
    kb.adjust(1)
    return kb.as_markup()


def build_caption(stats: dict) -> str:
    lines = [
        f"tracks cached: <b>{stats['total']}</b>",
        f"unique downloaders: <b>{stats['users']}</b>",
    ]
    if stats['by_entity']:
        entity = " · ".join(
            f"{ENTITY_LABELS.get(e, '?')}/{MODE_LABELS.get(m, '?')}: <b>{c}</b>"
            for (e, m), c in sorted(stats['by_entity'].items(), key=lambda kv: -kv[1])
        )
        lines.append(f"entity: {entity}")
    return "\n".join(lines)


async def render_page(page: str, track_repo: TrackRepository) -> tuple[BufferedInputFile, str]:
    stats = await track_repo.usage_stats()
    _, renderer = PAGES[page]
    banner = await asyncio.to_thread(renderer, stats)
    photo = BufferedInputFile(banner, filename=f"stats-{page}.png")
    return photo, build_caption(stats)


@router.callback_query(AdminPanelCallback.filter(F.path == AdminPanelPath.USAGE_STATS))
async def usage_stats(callback: CallbackQuery, track_repo: FromDishka[TrackRepository]):
    photo, caption = await render_page(DEFAULT_PAGE, track_repo)
    await callback.message.answer_photo(
        photo=photo,
        caption=caption,
        reply_markup=page_keyboard(DEFAULT_PAGE)
    )
    await callback.answer()


@router.callback_query(StatsPageCallback.filter())
async def switch_stats_page(
        callback: CallbackQuery,
        callback_data: StatsPageCallback,
        track_repo: FromDishka[TrackRepository]
):
    page = callback_data.page
    if page not in PAGES:
        await callback.answer()
        return
    photo, caption = await render_page(page, track_repo)
    await callback.message.edit_media(
        media=InputMediaPhoto(media=photo, caption=caption),
        reply_markup=page_keyboard(page)
    )
    await callback.answer()
