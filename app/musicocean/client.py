from app.musicocean.providers import DeezerClient
from app.config.settings import settings
from app.musicocean.enums import Provider


class MusicOceanClient:
    def __init__(
        self,
        deezer: bool = False,
        soundcloud: bool = False,
        youtube: bool = False,
        spotify: bool = False
    ):

        self.deezer = None
        self.soundcloud = None
        self.youtube = None
        self.spotify = None

        self.active = None
        self._ready = False

        if deezer:
            # TODO probably theres better way to check
            if settings.deezer.login and settings.deezer.password:
                self.deezer = DeezerClient(
                    settings.deezer.login,
                    settings.deezer.password
                )
        # ...
        else:
            raise "no providers specified"
    async def setup_all(self):
        if self.deezer:
            await self.deezer.setup()
        # ...
        self._ready = True

    # not sure if async is needed here
    async def set_provider(self, provider: Provider):
        match provider:
            case Provider.DEEZER:
                if not self.deezer:
                    raise "selected provider not specified"
                self.active = self.deezer
            # ...

