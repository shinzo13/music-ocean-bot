from app.bot.utils.search_results.get_track_results import get_track_results
from app.modules.musicocean.engines.shared.models import BaseTrackPreview
from app.modules.musicocean.enums.engine import Engine


def preview(track_id, title="t", preview_url=None) -> BaseTrackPreview:
    return BaseTrackPreview(
        id=track_id,
        title=title,
        artist_name="a",
        cover_url=None,
        preview_url=preview_url,
    )


async def test_drops_duplicate_ids_keeping_first_occurrence():
    matches = [preview(1, "first"), preview(2), preview(1, "dupe"), preview(3)]

    results = await get_track_results(Engine.DEEZER, matches, preview_covers=True)

    assert [r.id for r in results] == ["dz_tr_s_1", "dz_tr_s_2", "dz_tr_s_3"]
    assert results[0].title == "first"


async def test_ids_are_unique_even_when_everything_repeats():
    matches = [preview(7) for _ in range(10)]

    results = await get_track_results(Engine.DEEZER, matches, preview_covers=True)

    assert len(results) == 1
    assert len({r.id for r in results}) == len(results)


async def test_caps_at_fifty_after_deduplication():
    # 60 distinct tracks, each sent twice — telegram's limit applies to real ones
    matches = [preview(i) for i in range(60) for _ in range(2)]

    results = await get_track_results(Engine.DEEZER, matches, preview_covers=True)

    assert len(results) == 50
    assert [r.id for r in results] == [f"dz_tr_s_{i}" for i in range(50)]
