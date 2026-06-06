from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from dishka import FromDishka

from app.bot.callbacks.admin_panel_callback import AdminPanelCallback, AdminPanelPath
from app.database.repositories import UserRepository

router = Router()

class BanUserState(StatesGroup):
    user_id: str = State()


@router.callback_query(AdminPanelCallback.filter(F.path == AdminPanelPath.BAN_USER))
async def ban_user_callback(
        callback: CallbackQuery,
        state: FSMContext
):
    await callback.message.answer('enter id')
    await state.set_state(BanUserState.user_id)

@router.message(BanUserState.user_id)
async def ban_user_id_entered(
        message: Message,
        state: FSMContext,
        user_repo: FromDishka[UserRepository],
):
    user_id = int(message.text)
    user = await user_repo.get_user_by_id(user_id) \
        or await user_repo.add_user(user_id=user_id)
    user = await user_repo.update_user(user_id, is_banned=(not user.is_banned))
    await state.clear()
    await message.answer('banned' if user.is_banned else 'unbanned')


