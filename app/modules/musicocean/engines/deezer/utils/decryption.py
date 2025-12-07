# Decryption algorithm from: https://github.com/kmille/deezer-downloader

from Crypto.Hash import MD5
from Crypto.Cipher import Blowfish
from binascii import a2b_hex, b2a_hex
from asyncio import IncompleteReadError
from aiohttp import ClientResponse


def md5hex(data: bytes) -> bytes:
    h = MD5.new()
    h.update(data)
    return b2a_hex(h.digest())

def generate_track_key(track_id: int) -> str:
    key = b"g4el58wc0zvf9na1"
    track_id_md5 = md5hex(str(track_id).encode())
    xor_op = lambda i: chr(track_id_md5[i] ^ track_id_md5[i + 16] ^ key[i])
    decrypt_key = "".join([xor_op(i) for i in range(16)])
    return decrypt_key

def decrypt_chunk(data, key):
    iv = a2b_hex("0001020304050607")
    # TODO: singleton cipher object for multiple usage
    c = Blowfish.new(key.encode(), Blowfish.MODE_CBC, iv)
    return c.decrypt(data)

async def decrypt_track(resp: ClientResponse, track_id: int):
    key = generate_track_key(track_id)
    i = 0
    data = b''
    reading=True
    while reading:
        try:
            chunk = await resp.content.readexactly(2048)
        except IncompleteReadError:
            chunk = await resp.content.read(2048)
            reading=False
        if not chunk:
            break
        if ((i % 3) == 0) and len(chunk) == 2048:
            chunk = decrypt_chunk(chunk, key)
        data += chunk
        i += 1
    return data