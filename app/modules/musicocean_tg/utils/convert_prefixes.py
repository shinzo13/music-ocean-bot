from app.modules.musicocean.enums import Engine


def engine_to_prefix(engine: Engine) -> str:
    match engine:
        case Engine.DEEZER:
            return "dz"
        case Engine.SOUNDCLOUD:
            return "sc"
        case Engine.YOUTUBE:
            return "yt"
        case Engine.SPOTIFY:
            return "sp"
        case _:
            raise ValueError("invalid engine")


def prefix_to_engine(prefix: str) -> Engine:
    match prefix:
        case "dz":
            return Engine.DEEZER
        case "sc":
            return Engine.SOUNDCLOUD
        case "yt":
            return Engine.YOUTUBE
        case "sp":
            return Engine.SPOTIFY
        case _:
            raise ValueError("invalid engine prefix")
