from enum import StrEnum, auto

from aiogram.filters.callback_data import CallbackData


class AdminPanelPath(StrEnum):
    EXPORT_USERS = auto()
    MAILING = auto()
    BAN_USER = auto()
    USAGE_STATS = auto()


class AdminPanelCallback(CallbackData, prefix="admin"):
    path: AdminPanelPath
