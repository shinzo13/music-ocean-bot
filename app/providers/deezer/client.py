from typing import Any

from aiohttp import ClientSession

from app.providers.deezer.models import DeezerTrack
from app.providers.deezer.utils import get_arl
from app.providers.deezer.enums import DeezerAPIMethod
from app.providers.deezer.constants import *

class DeezerClient:
    def __init__(
            self,
            login: str,
            passwd: str,
            proxies: dict[str, str] = None # TODO
    ):
        self.login = login
        self.passwd = passwd

        self.session = None
        self.arl = None
        self.license_token = None
    async def setup(self):
        self.arl = await get_arl(
            self.login,
            self.passwd,
        )
        self.session = ClientSession(
            cookies={
                'arl': self.arl,
                'comeback': '1'
            },
            headers=HEADERS
        )

        options = (await (await self.session.get(
            USERDATA_URL
        )).json())['results']['USER']['OPTIONS']
        self.license_token = options['license_token']

    async def _api_request(
        self,
        method: DeezerAPIMethod,
        params: dict[str, Any],
    ) -> dict:
        async with self.session.get(
            f"{API_URL}/{method}",
            params=params,
        ) as resp:
            raw_data = await resp.json()
            if "error" in raw_data:
                raise # TODO separeted DeezerAPIException
            return raw_data # TODO data processing

















