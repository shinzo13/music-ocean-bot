import argparse
import asyncio
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config.settings import settings
from app.modules.musicocean.engines.deezer.client import DeezerClient


def _safe(name: str) -> str:
    return re.sub(r'[/\\:*?"<>|]', "_", name).strip()


async def _run(query: str, out_dir: Path, limit: int, index: int, list_only: bool) -> int:
    client = DeezerClient(
        settings.deezer.login.get_secret_value(),
        settings.deezer.password.get_secret_value(),
    )
    await client.setup()
    try:
        results = await client.search_tracks(query)
        if not results:
            print(f"ничего не найдено по запросу: {query}", file=sys.stderr)
            return 2

        if list_only:
            for i, t in enumerate(results[:limit]):
                print(f"{i}\t{t.artist_name} — {t.title}")
            return 0

        preview = results[index]
        track = await client.download_track(preview.id)

        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"{_safe(track.artist_name)} - {_safe(track.title)}.mp3"
        path.write_bytes(track.content)
        print(str(path))
        return 0
    finally:
        await client.close()


def main():
    p = argparse.ArgumentParser(description="скачать трек с deezer (через music-ocean-bot)")
    p.add_argument("query", help="название трека / артист")
    p.add_argument("-o", "--out", default="/home/shinrei/music", help="папка назначения")
    p.add_argument("-n", "--limit", type=int, default=10, help="сколько результатов показать при --list")
    p.add_argument("-i", "--index", type=int, default=0, help="какой из результатов качать (0 = первый)")
    p.add_argument("-l", "--list", action="store_true", help="только показать совпадения, не качать")
    a = p.parse_args()
    sys.exit(asyncio.run(_run(a.query, Path(a.out), a.limit, a.index, a.list)))


if __name__ == "__main__":
    main()
