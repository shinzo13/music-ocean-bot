import struct
from typing import Optional

from app.modules.musicocean.enums import Engine
from app.modules.musicocean.models import Track

def write_id3(
        track: Track,
        source: bytes,
        engine: Engine,
        watermark: Optional[str]
) -> bytes:
    frames = [
        frame("TIT2", text(track.title)),
        frame("TPE1", text(track.artist_name)),
        frame("TLEN", text(str(track.duration * 1000))),
        frame("APIC", picture(track.cover)),
    ]

    if watermark:
        frames.append(frame("COMM", comment("Source", watermark)))

    frames += [
        frame("COMM", comment("Engine", engine.value)),
        frame("COMM", comment("Inner ID", str(track.id)))
    ]

    id3 = b''.join(frames)
    header = struct.pack(">3sHBL", b"ID3", 0x0300, 0, synchsafe(len(frames)))
    return header + id3 + source


def synchsafe(n):
    return ((n << 3) & 0x7F000000) | ((n << 2) & 0x7F0000) | ((n << 1) & 0x7F00) | (n & 0x7F)


def frame(tag, data):
    return struct.pack(">4sLH", tag.encode(), len(data), 0) + data


def text(s):
    return b"\x03" + s.encode('utf-8')

def comment(desc: str, value: str):
    return (b"\x03" +
            b'eng' +
            desc.encode('utf-8') + b"\x00" +
            value.encode('utf-8'))



def picture(img):
    return b"\x00image/jpeg\x00\x03\x00" + img
