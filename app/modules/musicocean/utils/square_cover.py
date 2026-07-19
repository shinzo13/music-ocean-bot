import io

from PIL import Image

SIZE = 320


def _trim_black_borders(img: Image.Image) -> Image.Image:
    # yt bakes letterbox/pillarbox bars into thumbnails of non-16:9 videos;
    # keep only the region that has any non-near-black pixels
    mask = img.convert("L").point(lambda p: 255 if p > 24 else 0)
    bbox = mask.getbbox()
    if bbox and (bbox[2] - bbox[0]) >= 32 and (bbox[3] - bbox[1]) >= 32:
        img = img.crop(bbox)
    return img


def square_cover(image: bytes) -> bytes:
    img = Image.open(io.BytesIO(image)).convert("RGB")
    img = _trim_black_borders(img)
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
