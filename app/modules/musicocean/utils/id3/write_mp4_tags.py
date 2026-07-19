import av
import io

from app.modules.musicocean.engines.shared.models import BaseTrack


def write_mp4_tags(track: BaseTrack, source: bytes, watermark: str | None = None) -> bytes:
    # itag 140 is already aac — remux with packet copy instead of re-encoding
    in_buf = io.BytesIO(source)
    out_buf = io.BytesIO()

    with av.open(in_buf, 'r') as in_container:
        with av.open(out_buf, 'w', format='ipod') as out_container:
            in_stream = in_container.streams.audio[0]
            out_stream = out_container.add_stream_from_template(in_stream)
            out_container.metadata.update({
                'title': track.title,
                'artist': track.artist_name,
            })
            if watermark:
                out_container.metadata['comment'] = watermark

            for packet in in_container.demux(in_stream):
                if packet.dts is None:
                    continue
                packet.stream = out_stream
                out_container.mux(packet)

    return out_buf.getvalue()
