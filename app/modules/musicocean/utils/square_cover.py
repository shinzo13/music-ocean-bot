import io

from PIL import Image

SIZE = 320


def square_cover(image: bytes) -> bytes:
    img = Image.open(io.BytesIO(image)).convert("RGB")
    w, h = img.size
    side = min(w, h)
    img = img.crop((
        (w - side) // 2,
        (h - side) // 2,
        (w + side) // 2,
        (h + side) // 2,
    ))
    if side > SIZE:
        img = img.resize((SIZE, SIZE), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=88)
    return buf.getvalue()
