from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data == "feature_not_available")
async def spotify_scrobbling_handler(
        callback: CallbackQuery
):
    await callback.answer(
        "🔒 This feature is not available at the moment.",
        show_alert=True
    )