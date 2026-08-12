from app.config.settings import settings
from app.modules.musicocean.enums import Engine


def fallback_engine() -> Engine:
    if settings.engines.is_enabled(Engine.DEEZER):
        return Engine.DEEZER
    return next((e for e in Engine if settings.engines.is_enabled(e)), Engine.DEEZER)
