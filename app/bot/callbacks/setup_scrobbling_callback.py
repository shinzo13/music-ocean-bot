from aiogram.filters.callback_data import CallbackData


class SetupScrobblingCallback(CallbackData, prefix='scrobbling'):
    init: bool
    approved: bool
