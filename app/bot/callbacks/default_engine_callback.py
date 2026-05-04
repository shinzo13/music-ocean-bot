from aiogram.filters.callback_data import CallbackData


class DefaultEngineCallback(CallbackData, prefix='engine'):
    engine_prefix: str