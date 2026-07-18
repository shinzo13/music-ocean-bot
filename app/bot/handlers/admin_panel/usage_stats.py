import asyncio

from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile
from dishka import FromDishka

from app.bot.callbacks.admin_panel_callback import AdminPanelCallback, AdminPanelPath
from app.bot.utils.stats_banner import render_stats_banner
from app.database.models.download_context import EntityType, DownloadMode
from app.database.repositories import TrackRepository

router = Router()

ENTITY_LABELS = {
    EntityType.ALBUM: "album",
    EntityType.PLAYLIST: "playlist",
    EntityType.ARTIST: "artist",
}

MODE_LABELS = {
    DownloadMode.SINGLE: "single",
    DownloadMode.MULTI: "multi",
}


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


@router.callback_query(AdminPanelCallback.filter(F.path == AdminPanelPath.USAGE_STATS))
async def usage_stats(callback: CallbackQuery, track_repo: FromDishka[TrackRepository]):
    stats = await track_repo.usage_stats()
    banner = await asyncio.to_thread(
        render_stats_banner,
        {e.value.lower(): c for e, c in stats['by_engine'].items()},
        {ctx.value.lower(): c for ctx, c in stats['by_context'].items()},
    )
    await callback.message.answer_photo(
        photo=BufferedInputFile(banner, filename="usage-stats.png"),
        caption=build_caption(stats)
    )
    await callback.answer()
