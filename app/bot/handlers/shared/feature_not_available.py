from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext

router = Router()


@router.callback_query(F.data == "feature_not_available")
async def spotify_scrobbling_handler(
        callback: CallbackQuery,
        i18n: I18nContext
):
    await callback.answer(
        i18n.get('feature-not-available'),
        show_alert=True
    )
