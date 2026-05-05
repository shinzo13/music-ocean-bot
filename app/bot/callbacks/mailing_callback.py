from aiogram.filters.callback_data import CallbackData


class MailingCallback(CallbackData, prefix='mail'):
    approved: bool
