import io

from mutagen.id3 import ID3, TIT2, TPE1, APIC, COMM
from mutagen.mp3 import MP3

from app.modules.musicocean.engines.shared.models import BaseTrack


def write_mp3_tags(
        track: BaseTrack,
        source: bytes,
        watermark: str | None = None
) -> bytes:
    buf = io.BytesIO(source)
    audio = MP3(buf, ID3=ID3)
    if audio.tags is None:
        audio.add_tags()
    audio.tags.add(TIT2(encoding=3, text=track.title))
    audio.tags.add(TPE1(encoding=3, text=track.artist_name))
    if track.cover:
        audio.tags.add(APIC(encoding=3, mime='image/jpeg',
                           type=3, desc='', data=track.cover))
    if watermark:
        audio.tags.add(COMM(encoding=3, lang='eng',
                           desc='', text=watermark))
    out = io.BytesIO()
    audio.save(out)
    return out.getvalue()