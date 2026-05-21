from typing import Optional

from shazamio import Shazam

# rust version is a bit broken
Shazam.recognize_song = Shazam.recognize_song.__wrapped__ # noqa

async def shazam_wrapped(audio: bytes) -> Optional[tuple[str,str]]:
  resp = await Shazam().recognize_song(audio)
  if not resp['matches']:
      return None
  return resp['track']['title'], resp['track']['subtitle']