from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from app.config.log import get_logger

logger = get_logger(__name__)

# idempotent hand-rolled migrations; create_all only creates missing tables,
# so column additions on existing tables live here
STATEMENTS = [
    """DO $$ BEGIN
        CREATE TYPE download_context_enum AS ENUM ('SEARCH', 'LINK', 'LASTFM', 'ENTITY');
    EXCEPTION WHEN duplicate_object THEN NULL; END $$""",
    """DO $$ BEGIN
        CREATE TYPE entity_type_enum AS ENUM ('ALBUM', 'PLAYLIST', 'ARTIST');
    EXCEPTION WHEN duplicate_object THEN NULL; END $$""",
    """DO $$ BEGIN
        CREATE TYPE download_mode_enum AS ENUM ('SINGLE', 'MULTI');
    EXCEPTION WHEN duplicate_object THEN NULL; END $$""",
    "ALTER TABLE base_tracks ADD COLUMN IF NOT EXISTS download_context download_context_enum",
    "ALTER TABLE base_tracks ADD COLUMN IF NOT EXISTS entity_type entity_type_enum",
    "ALTER TABLE base_tracks ADD COLUMN IF NOT EXISTS download_mode download_mode_enum",
    # backfill pre-context rows: spotify came from lastfm matching,
    # youtube from link downloads, everything else from plain search
    "UPDATE base_tracks SET download_context = 'LASTFM' WHERE download_context IS NULL AND engine = 'SPOTIFY'",
    "UPDATE base_tracks SET download_context = 'LINK' WHERE download_context IS NULL AND engine = 'YOUTUBE'",
    "UPDATE base_tracks SET download_context = 'SEARCH' WHERE download_context IS NULL",
    "ALTER TABLE base_tracks ALTER COLUMN download_context SET NOT NULL",
    "ALTER TABLE base_tracks ALTER COLUMN download_context SET DEFAULT 'SEARCH'",
    "ALTER TABLE base_tracks ADD COLUMN IF NOT EXISTS download_speed double precision",
    # create_all never extends existing enums — yandex was added after the type
    "ALTER TYPE engine_enum ADD VALUE IF NOT EXISTS 'YANDEX'",
]


async def run_migrations(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        for stmt in STATEMENTS:
            await conn.execute(text(stmt))
    logger.info("Migrations applied")
