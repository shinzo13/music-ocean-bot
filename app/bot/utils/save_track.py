from app.database.models.download_context import DownloadContext, EntityType, DownloadMode
from app.database.repositories import TrackRepository
from app.modules.musicocean.enums.engine import Engine
from app.modules.musicocean_tg.models.cached_track import CachedTrack


async def save_track_with_source(
        track_repo: TrackRepository,
        engine: Engine,
        track_id: int | str,
        cached: CachedTrack,
        file_id: str,
        file_unique_id: str | None,
        user_id: int,
        download_context: DownloadContext,
        entity_type: EntityType | None = None,
        download_mode: DownloadMode | None = None
) -> None:
    kwargs = dict(
        download_speed=cached.download_speed,
        telegram_file_id=file_id,
        telegram_file_unique_id=file_unique_id,
        user_id=user_id,
        download_context=download_context,
        entity_type=entity_type,
        download_mode=download_mode
    )
    if not await track_repo.get_track(track_id, engine):
        await track_repo.add_track(engine=engine, track_id=track_id, **kwargs)
    # spotify audio comes from another engine — cache the real source row too
    if cached.source_engine is not None and cached.source_engine != engine:
        if not await track_repo.get_track(cached.source_id, cached.source_engine):
            await track_repo.add_track(
                engine=cached.source_engine, track_id=cached.source_id, **kwargs
            )
