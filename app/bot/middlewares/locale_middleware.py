from aiogram_i18n import I18nMiddleware
from aiogram_i18n.managers import BaseManager

from app.database.models import User as DatabaseUser


class PatchedManager(BaseManager):
    def __init__(
            self,
            default_locale: str | None = 'en',
    ):
        super().__init__(default_locale=default_locale)

    async def set_locale(self, locale: str) -> None:
        pass

    async def get_locale(self, **kwargs) -> str:
        if kwargs.get('user') is not None:
            user: DatabaseUser = kwargs.get('user')
            return user.settings.locale or self.default_locale
        return self.default_locale


class LocaleMiddleware(I18nMiddleware):
    ...
