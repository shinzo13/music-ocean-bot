from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message
from aiogram_i18n import I18nContext
from dishka import FromDishka

from app.bot.callbacks.admin_panel_callback import AdminPanelCallback, AdminPanelPath
from app.bot.callbacks.mailing_callback import MailingCallback
from app.bot.keyboards.mailing import mailing_approve_keyboard, mailing_back_keyboard
from app.config.log import get_logger
from app.database.repositories import UserRepository

logger = get_logger(__name__)


MAILING_CONTENT_TYPES = [
    ContentType.RICH_MESSAGE,
    ContentType.TEXT,
    ContentType.ANIMATION,
    ContentType.DOCUMENT,
    ContentType.PHOTO,
    ContentType.STICKER,
    ContentType.VIDEO,
]

class MailingState(StatesGroup):
    message = State()
    buttons = State()
    approving = State()


router = Router()


@router.callback_query(AdminPanelCallback.filter(F.path == AdminPanelPath.MAILING))
async def mailing(
        callback: CallbackQuery,
        state: FSMContext,
        i18n: I18nContext
):
    await state.set_state(MailingState.message)
    await callback.message.edit_text(
        i18n.get('mailing-enter-message'),
        reply_markup=mailing_back_keyboard()
    )


@router.message(MailingState.message)
async def mailing_message(
        message: Message,
        state: FSMContext,
        i18n: I18nContext
):
    if message.content_type not in MAILING_CONTENT_TYPES:
        await message.answer(
            i18n.get('mailing-restricted-content-type'),
            reply_markup=mailing_back_keyboard()
        )
        return

    await state.update_data(message=message)
    await message.answer(i18n.get('mailing-enter-buttons'))
    await state.set_state(MailingState.buttons)


@router.message(MailingState.buttons)
async def mailing_buttons(
        message: Message,
        state: FSMContext,
        i18n: I18nContext
):
    try:
        kb = []
        # one button per line: "name - link"
        for btn in (message.text or '').splitlines():
            if not btn.strip():
                continue
            btn_name, btn_link = btn.split(' - ', maxsplit=1)
            kb.append([InlineKeyboardButton(text=btn_name.strip(), url=btn_link.strip())])
        if not kb:
            raise ValueError('no buttons')
    except ValueError:
        await message.answer(
            i18n.get('mailing-invalid-format'),
            reply_markup=mailing_back_keyboard()
        )
        return
    buttons = InlineKeyboardMarkup(inline_keyboard=kb)
    await state.update_data(buttons=buttons)
    msg: Message = await state.get_value('message')
    await msg.send_copy(
        message.from_user.id,
        reply_markup=buttons
    )
    await message.answer(
        i18n.get('mailing-approve-message'),
        reply_markup=mailing_approve_keyboard()
    )
    await state.set_state(MailingState.approving)

@router.callback_query(MailingState.approving, MailingCallback.filter())
async def mailing_approved(
        query: CallbackQuery,
        callback_data: MailingCallback,
        i18n: I18nContext,
        state: FSMContext,
        user_repo: FromDishka[UserRepository],
):
    if not callback_data.approved:
        await query.message.edit_text(i18n.get('mailing-canceled'))
        await state.clear()
        return

    await query.message.answer(i18n.get('mailing-sending'))
    all_users = 0
    succeed = 0
    msg: Message = await state.get_value('message')
    async for user_id in user_repo.get_all_users(for_mailing=True):
        all_users += 1
        try:
            await msg.copy_to(
                user_id,
                reply_markup=None  # TODO
            )
            succeed += 1
        except Exception as err:  # TODO more specified
            logger.error(f"Error sending message to {user_id}: {err}")
            await user_repo.update_user(user_id, is_dm=False)

    await query.message.answer(
        i18n.get(
            'mailing-finished',
            succeed=succeed,
            all=all_users
        )
    )
