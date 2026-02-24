from app.bot.constants import DEEZER_EMOJI, SOUNDCLOUD_EMOJI, YOUTUBE_EMOJI, SPOTIFY_EMOJI
from app.modules.musicocean.enums import Engine


def get_engine_emoji(engine: Engine):
    match engine:
        case Engine.DEEZER:
            return DEEZER_EMOJI
        case Engine.SOUNDCLOUD:
            return SOUNDCLOUD_EMOJI
        case Engine.YOUTUBE:
            return YOUTUBE_EMOJI
        case Engine.SPOTIFY:
            return SPOTIFY_EMOJI
        case _:
            raise ValueError("invalid engine")