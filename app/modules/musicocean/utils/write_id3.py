import struct

from app.modules.musicocean.models import Track


def write_id3(
        track: Track,
        source: bytes
) -> bytes:
    frames = b''.join([
        frame("TIT2", text(track.title)),
        frame("TPE1", text(track.artist_name)),
        frame("TLEN", text(str(track.duration * 1000))),
        frame("APIC", picture(track.cover)),
    ])

    header = struct.pack(">3sHBL", b"ID3", 0x0300, 0, synchsafe(len(frames)))
    return header + frames + source

def synchsafe(n):
    return ((n << 3) & 0x7F000000) | ((n << 2) & 0x7F0000) | ((n << 1) & 0x7F00) | (n & 0x7F)

def frame(tag, data):
    return struct.pack(">4sLH", tag.encode(), len(data), 0) + data

def text(s):
    return b"\x03" + s.encode('utf-8')

def picture(img):
    return b"\x00image/jpeg\x00\x03\x00" + img