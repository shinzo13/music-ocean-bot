from enum import StrEnum, auto

from aiogram.filters.callback_data import CallbackData


class MainMenuPath(StrEnum):
    SELF = auto()
    GUIDE = auto()
    PROFILE = auto()
    SETTINGS = auto()
    ADMIN_PANEL = auto()


class MainMenuCallback(CallbackData, prefix="menu"):
    path: str