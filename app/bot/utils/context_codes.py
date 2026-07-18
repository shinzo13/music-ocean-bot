from app.database.models.download_context import DownloadContext, EntityType, DownloadMode

# short context codes embedded in inline result ids:
# {engine}_tr_{code}_{track_id}
CTX_CODES: dict[str, tuple[DownloadContext, EntityType | None, DownloadMode | None]] = {
    "s": (DownloadContext.SEARCH, None, None),
    "l": (DownloadContext.LINK, None, None),
    "f": (DownloadContext.LASTFM, None, None),
    "ea": (DownloadContext.ENTITY, EntityType.ALBUM, DownloadMode.SINGLE),
    "ep": (DownloadContext.ENTITY, EntityType.PLAYLIST, DownloadMode.SINGLE),
    "er": (DownloadContext.ENTITY, EntityType.ARTIST, DownloadMode.SINGLE),
}
