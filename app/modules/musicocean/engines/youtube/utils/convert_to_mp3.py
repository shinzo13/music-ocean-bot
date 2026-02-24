import av
import io


def convert_to_mp3(source: bytes) -> bytes:
    in_buf = io.BytesIO(source)
    out_buf = io.BytesIO()

    with av.open(in_buf) as in_container:
        with av.open(out_buf, 'w', format='mp3') as out_container:
            in_stream = in_container.streams.audio[0]
            out_stream = out_container.add_stream('mp3', rate=in_stream.rate)

            for packet in in_container.demux(in_stream):
                try:
                    for frame in packet.decode():
                        for out_packet in out_stream.encode(frame):
                            out_container.mux(out_packet)
                except EOFError:
                    break

            for out_packet in out_stream.encode(None):
                out_container.mux(out_packet)

    return out_buf.getvalue()