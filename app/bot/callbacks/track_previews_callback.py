from aiogram.filters.callback_data import CallbackData


class TrackPreviewsCallback(CallbackData, prefix='previews'):
    show_covers: bool