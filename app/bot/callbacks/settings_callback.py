from enum import StrEnum, auto

from aiogram.filters.callback_data import CallbackData


class SettingsPath(StrEnum):
    ENGINE = auto()
    PREVIEWS = auto()
    SCROBBLING = auto()

class SettingsCallback(CallbackData, prefix='settings'):
    path: SettingsPath