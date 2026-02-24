from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from dishka import FromDishka

from app.database.repositories import UserRepository
from app.bot.keyboards.mailing import mailing_approve_keyboard

router = Router()

class MailingState(StatesGroup):
    message = State()
    buttons = State()
    approving = State()


@router.callback_query(F.data=="mailing")
async def mailing(
        callback: CallbackQuery,
        user_repo: FromDishka[UserRepository],
        state: FSMContext,
):
    await state.set_state(MailingState.message)
    await callback.message.edit_text(
        "Send a message for mailing:"
    )


@router.message(MailingState.message)
async def mailing_message(message: Message, state: FSMContext):
    await state.update_data(message=message)
    await state.set_state(MailingState.buttons)
    await message.answer(
        f"msg: {message.text}",
        reply_markup=mailing_approve_keyboard()
    )

# todo buttons state
#@router.callback_query(MailingState.approving)


@router.callback_query(MailingState.approving)
async def mailing_approve(callback: CallbackQuery, state: FSMContext):
    if callback.data == "mailing_approve":
        await callback.message.edit_text("sending to all users")
        # todo send to all users
        await callback.message.answer("Sent to ALLLLLLLLLL users")
    else:
        await callback.message.edit_text("Canceled")
    await state.clear()