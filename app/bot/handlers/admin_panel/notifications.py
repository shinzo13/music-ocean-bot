from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from dishka import FromDishka

from app.bot.callbacks.admin_panel_callback import AdminPanelCallback, AdminPanelPath
from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath
from app.bot.constants import BACK_EMOJI_ID
from app.database.repositories import UserRepository

router = Router()


class NotificationsToggleCallback(CallbackData, prefix="adm_notif"):
    enable: bool


def _view(enabled: bool) -> tuple[str, InlineKeyboardMarkup]:
    state = "включены ✅" if enabled else "выключены ❌"
    text = (
        f"<b>Уведомления о загрузках</b>\n\n"
        f"Присылать тебе уведомление, когда кто-то что-то скачал.\n\n"
        f"Сейчас: <b>{state}</b>"
    )
    toggle = "Выключить" if enabled else "Включить"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=toggle,
            callback_data=NotificationsToggleCallback(enable=not enabled).pack(),
        )],
        [InlineKeyboardButton(
            text="назад",
            callback_data=MainMenuCallback(path=MainMenuPath.ADMIN_PANEL).pack(),
            icon_custom_emoji_id=BACK_EMOJI_ID,
        )],
    ])
    return text, kb


@router.callback_query(AdminPanelCallback.filter(F.path == AdminPanelPath.NOTIFICATIONS))
async def notifications_menu(callback: CallbackQuery, user_repo: FromDishka[UserRepository]):
    user = await user_repo.get_user_by_id(callback.from_user.id)
    enabled = bool(user and user.settings.admin_download_notifications)
    text, kb = _view(enabled)
    await callback.message.edit_text(text=text, reply_markup=kb)


@router.callback_query(NotificationsToggleCallback.filter())
async def notifications_toggle(
        callback: CallbackQuery,
        callback_data: NotificationsToggleCallback,
        user_repo: FromDishka[UserRepository],
):
    await user_repo.update_user_settings(
        callback.from_user.id,
        admin_download_notifications=callback_data.enable,
    )
    text, kb = _view(callback_data.enable)
    await callback.message.edit_text(text=text, reply_markup=kb)
    await callback.answer("Готово")
