from aiohttp import ClientSession

from app.providers.deezer.utils.get_arl import get_arl
from app.providers.deezer import enums
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
            headers=headers
        )

        options = (await (await self.session.get(
            USERDATA_URL
        )).json())['results']['USER']['OPTIONS']
        self.license_token = options['license_token']

