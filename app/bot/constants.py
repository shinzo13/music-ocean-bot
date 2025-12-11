from app.modules.musicocean.enums import Engine, EntityType

ENGINE_PREFIXES = {
    Engine.DEEZER: "dz",
    Engine.SOUNDCLOUD: "sc",
    Engine.YOUTUBE: "yt",
    Engine.SPOTIFY: "sp"
}

ENTITY_PREFIXES = {
    EntityType.ALBUM: "al",
    EntityType.ARTIST: "ar",
    EntityType.PLAYLIST: "pl"
}
