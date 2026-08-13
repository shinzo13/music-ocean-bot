from dataclasses import dataclass
from typing import Optional

from app.bot.utils.context_codes import CTX_CODES
from app.database.models.download_context import DownloadContext, DownloadMode, EntityType
from app.modules.musicocean.enums.engine import Engine

ENGINE_PREFIXES = {
    "dz": Engine.DEEZER,
    "sc": Engine.SOUNDCLOUD,
    "yt": Engine.YOUTUBE,
    "sp": Engine.SPOTIFY,
    "ya": Engine.YANDEX,
}

# yandex ids travel as strings (playlists carry an owner prefix), the rest are ints
NUMERIC_ID_ENGINES = (Engine.DEEZER, Engine.SOUNDCLOUD)


@dataclass(frozen=True)
class TrackRef:
    engine: Engine
    track_id: int | str
    download_context: DownloadContext
    entity_type: EntityType | None
    download_mode: DownloadMode | None


def parse_track_ref(ref: str) -> Optional[TrackRef]:
    """Reads {engine}_tr_{ctx}_{track_id}, the id shared by inline results and
    the download button. Returns None for anything else — usage guides and
    other callbacks travel through the same channel."""
    parts = ref.split("_", maxsplit=3)
    if len(parts) < 3 or parts[1] != "tr":
        return None

    engine = ENGINE_PREFIXES.get(parts[0])
    if engine is None:
        return None

    # new ids carry a context code; ids cached by telegram before the rollout
    # lack it — treat those as plain search
    if len(parts) == 4 and parts[2] in CTX_CODES:
        context, entity_type, mode = CTX_CODES[parts[2]]
        track_id: int | str = parts[3]
    else:
        context, entity_type, mode = DownloadContext.SEARCH, None, None
        track_id = ref.split("_", maxsplit=2)[2]

    if engine in NUMERIC_ID_ENGINES:
        try:
            track_id = int(track_id)
        except ValueError:
            return None

    return TrackRef(engine, track_id, context, entity_type, mode)
