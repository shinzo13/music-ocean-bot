from aiogram.filters.callback_data import CallbackData


class LocalesCallback(CallbackData, prefix='locale'):
    code: str