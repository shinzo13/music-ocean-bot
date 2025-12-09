import asyncio
from rich import print

from app.modules.musicocean.engines.deezer import DeezerClient

dz = DeezerClient(
    login="airu2is838sjww@proton.me",
    password="rx^B2&sklfVHQX4M"
)

async def main():
    await dz.setup()
    track = (await dz.search_tracks("zavet paranoia"))[0]
    bts = (await dz.download_track(track_id=track.id))
    with open("paranoia.mp3", "wb") as f:
        f.write(bts.content)

asyncio.run(main())