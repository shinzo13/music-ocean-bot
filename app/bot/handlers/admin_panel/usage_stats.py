from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from dishka import FromDishka

from app.bot.callbacks.admin_panel_callback import AdminPanelCallback, AdminPanelPath
from app.database.models.download_context import DownloadContext, EntityType, DownloadMode
from app.database.repositories import TrackRepository

router = Router()

CONTEXT_LABELS = {
    DownloadContext.SEARCH: "🔍 search",
    DownloadContext.LINK: "🔗 link",
    DownloadContext.LASTFM: "📻 last.fm",
    DownloadContext.ENTITY: "📀 entity",
}

ENTITY_LABELS = {
    EntityType.ALBUM: "album",
    EntityType.PLAYLIST: "playlist",
    EntityType.ARTIST: "artist",
}

MODE_LABELS = {
    DownloadMode.SINGLE: "single",
    DownloadMode.MULTI: "multi",
}


def _bar(count: int, total: int, width: int = 8) -> str:
    if total == 0:
        return "░" * width
    filled = round(count / total * width)
    return "▓" * filled + "░" * (width - filled)


def render_stats(stats: dict) -> str:
    total = stats['total']
    lines = [
        "<b>📊 usage stats</b>",
        "",
        f"tracks cached: <b>{total}</b>",
        f"unique downloaders: <b>{stats['users']}</b>",
        "",
        "<b>by download context</b>",
    ]

    for ctx in DownloadContext:
        count = stats['by_context'].get(ctx, 0)
        pct = f"{count / total * 100:.0f}%" if total else "0%"
        lines.append(f"<code>{_bar(count, total)}</code> {CONTEXT_LABELS[ctx]} — <b>{count}</b> ({pct})")

    if stats['by_entity']:
        lines += ["", "<b>entity breakdown</b>"]
        for (entity, mode), count in sorted(
                stats['by_entity'].items(), key=lambda kv: -kv[1]
        ):
            entity_label = ENTITY_LABELS.get(entity, "?")
            mode_label = MODE_LABELS.get(mode, "?")
            lines.append(f"· {entity_label} / {mode_label} — <b>{count}</b>")

    lines += ["", "<b>by engine</b>"]
    for engine, count in sorted(stats['by_engine'].items(), key=lambda kv: -kv[1]):
        lines.append(f"· {engine.value.lower()} — <b>{count}</b>")

    return "\n".join(lines)


@router.callback_query(AdminPanelCallback.filter(F.path == AdminPanelPath.USAGE_STATS))
async def usage_stats(callback: CallbackQuery, track_repo: FromDishka[TrackRepository]):
    stats = await track_repo.usage_stats()
    try:
        await callback.message.answer(render_stats(stats))
    except TelegramBadRequest:
        pass
    await callback.answer()
