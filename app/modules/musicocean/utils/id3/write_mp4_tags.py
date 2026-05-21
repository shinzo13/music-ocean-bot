import av
import io

from app.modules.musicocean.engines.shared.models import BaseTrack


def write_mp4_tags(track: BaseTrack, source: bytes, watermark: str | None = None) -> bytes:
    in_buf = io.BytesIO(source)
    out_buf = io.BytesIO()

    with av.open(in_buf, 'r') as in_container:
        with av.open(out_buf, 'w', format='ipod') as out_container:
            out_stream = out_container.add_stream('aac', rate=in_container.streams.audio[0].rate)
            out_container.metadata.update({
                'title': track.title,
                'artist': track.artist_name,
            })
            if watermark:
                out_container.metadata['comment'] = watermark

            for packet in in_container.demux():
                if packet.dts is None:
                    continue
                for frame in packet.decode():
                    for out_packet in out_stream.encode(frame):
                        out_container.mux(out_packet)

            for out_packet in out_stream.encode(None):
                out_container.mux(out_packet)

    return out_buf.getvalue()