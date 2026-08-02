from aiogram import Router, F
from aiogram.exceptions import TelegramAPIError
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram_i18n import I18nContext
from dishka import FromDishka

from app.bot.callbacks.admin_panel_callback import AdminPanelCallback, AdminPanelPath
from app.bot.callbacks.main_menu_callback import MainMenuCallback, MainMenuPath
from app.bot.constants import BACK_EMOJI_ID, BAN_EMOJI_ID
from app.config.log import get_logger
from app.database.models import User
from app.database.repositories import UserRepository

logger = get_logger(__name__)

router = Router()

PAGE_SIZE = 8


class BannedListCallback(CallbackData, prefix="banlist"):
    page: int


class BannedUserCallback(CallbackData, prefix="banuser"):
    user_id: int
    page: int


class UnbanCallback(CallbackData, prefix="unban"):
    user_id: int
    page: int


class BanUserState(StatesGroup):
    target = State()


def parse_target(text: str) -> tuple[str, str]:
    """Split admin input into ('id' | 'username', value).

    Anything that is all digits (optionally signed) counts as a telegram id,
    everything else is treated as a username — with or without the leading @.
    """
    raw = (text or '').strip()
    if raw.startswith('@'):
        return 'username', raw.lstrip('@').strip()
    if raw.lstrip('-').isdigit():
        return 'id', raw
    return 'username', raw


def user_label(user: User) -> str:
    """@handle when we know it, otherwise a name, otherwise the bare id."""
    if user.username:
        return f'@{user.username}'
    name = ' '.join(filter(None, (user.first_name, user.last_name))).strip()
    return name or str(user.user_id)


def banned_list_view(users: list[User], total: int, page: int) -> tuple[str, InlineKeyboardMarkup]:
    pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    if total == 0:
        text = '<b>Banned users</b>\n\nnobody is banned right now.'
    else:
        lines = [f'<b>Banned users</b> — {total} total (page {page + 1}/{pages})', '']
        lines += [f'• {user_label(user)} — <code>{user.user_id}</code>' for user in users]
        text = '\n'.join(lines)

    rows = [
        [InlineKeyboardButton(
            text=user_label(user),
            callback_data=BannedUserCallback(user_id=user.user_id, page=page).pack(),
        )]
        for user in users
    ]

    if pages > 1:
        nav = []
        if page > 0:
            nav.append(InlineKeyboardButton(
                text='◀️', callback_data=BannedListCallback(page=page - 1).pack()
            ))
        if page + 1 < pages:
            nav.append(InlineKeyboardButton(
                text='▶️', callback_data=BannedListCallback(page=page + 1).pack()
            ))
        rows.append(nav)

    rows.append([InlineKeyboardButton(
        text='ban someone',
        callback_data=AdminPanelCallback(path=AdminPanelPath.BAN_USER).pack(),
        icon_custom_emoji_id=BAN_EMOJI_ID,
    )])
    rows.append([InlineKeyboardButton(
        text='back',
        callback_data=MainMenuCallback(path=MainMenuPath.ADMIN_PANEL).pack(),
        icon_custom_emoji_id=BACK_EMOJI_ID,
    )])
    return text, InlineKeyboardMarkup(inline_keyboard=rows)


def banned_user_view(user: User, page: int) -> tuple[str, InlineKeyboardMarkup]:
    name = ' '.join(filter(None, (user.first_name, user.last_name))).strip()
    lines = [f'<b>{user_label(user)}</b>', '', f'• id: <code>{user.user_id}</code>']
    if name:
        lines.append(f'• name: {name}')
    if user.username:
        lines.append(f'• username: @{user.username}')
    lines.append(f'• locale: <code>{user.settings.locale or "—"}</code>')

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text='unban',
            callback_data=UnbanCallback(user_id=user.user_id, page=page).pack(),
        )],
        [InlineKeyboardButton(
            text='back to list',
            callback_data=BannedListCallback(page=page).pack(),
            icon_custom_emoji_id=BACK_EMOJI_ID,
        )],
    ])
    return '\n'.join(lines), kb


async def show_list(message: Message, user_repo: UserRepository, page: int, edit: bool = True):
    total = await user_repo.count_banned()
    pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page = min(max(page, 0), pages - 1)
    users = await user_repo.get_banned_users(limit=PAGE_SIZE, offset=page * PAGE_SIZE)
    text, kb = banned_list_view(users, total, page)
    if edit:
        await message.edit_text(text=text, reply_markup=kb)
    else:
        await message.answer(text=text, reply_markup=kb)


async def notify_unbanned(callback: CallbackQuery, i18n: I18nContext, user: User) -> bool:
    """Tell the user they are back in, in their own language."""
    locale = user.settings.locale or i18n.core.default_locale
    try:
        await callback.bot.send_message(user.user_id, i18n.get('unban-notice', locale))
        return True
    except TelegramAPIError as err:
        # blocked the bot, never started it, deleted account — not worth failing over
        logger.info(f"could not notify {user.user_id} about unban: {err}")
        return False


@router.callback_query(AdminPanelCallback.filter(F.path == AdminPanelPath.BANNED_USERS))
async def banned_users(
        callback: CallbackQuery,
        state: FSMContext,
        user_repo: FromDishka[UserRepository],
):
    await state.clear()
    await show_list(callback.message, user_repo, page=0)
    await callback.answer()


@router.callback_query(BannedListCallback.filter())
async def banned_users_page(
        callback: CallbackQuery,
        callback_data: BannedListCallback,
        user_repo: FromDishka[UserRepository],
):
    await show_list(callback.message, user_repo, page=callback_data.page)
    await callback.answer()


@router.callback_query(BannedUserCallback.filter())
async def banned_user_card(
        callback: CallbackQuery,
        callback_data: BannedUserCallback,
        user_repo: FromDishka[UserRepository],
):
    user = await user_repo.get_user_by_id(callback_data.user_id)
    if user is None or not user.is_banned:
        await callback.answer('already unbanned')
        await show_list(callback.message, user_repo, page=callback_data.page)
        return
    text, kb = banned_user_view(user, callback_data.page)
    await callback.message.edit_text(text=text, reply_markup=kb)
    await callback.answer()


@router.callback_query(UnbanCallback.filter())
async def unban_user(
        callback: CallbackQuery,
        callback_data: UnbanCallback,
        i18n: I18nContext,
        user_repo: FromDishka[UserRepository],
):
    user = await user_repo.get_user_by_id(callback_data.user_id)
    if user is None:
        await callback.answer('no such user')
        return

    user = await user_repo.update_user(user.user_id, is_banned=False)
    delivered = await notify_unbanned(callback, i18n, user)

    await callback.answer('unbanned' if delivered else 'unbanned (could not notify)')
    await show_list(callback.message, user_repo, page=callback_data.page)


@router.callback_query(AdminPanelCallback.filter(F.path == AdminPanelPath.BAN_USER))
async def ban_user_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BanUserState.target)
    await callback.message.answer(
        'send a <b>@username</b> or a numeric <b>id</b> of the user to ban.',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text='cancel',
                callback_data=AdminPanelCallback(path=AdminPanelPath.BANNED_USERS).pack(),
                icon_custom_emoji_id=BACK_EMOJI_ID,
            )
        ]])
    )
    await callback.answer()


@router.message(BanUserState.target)
async def ban_user_target_entered(
        message: Message,
        state: FSMContext,
        user_repo: FromDishka[UserRepository],
):
    kind, value = parse_target(message.text or '')

    if kind == 'username':
        user = await user_repo.get_user_by_username(value)
        if user is None:
            await message.answer(
                f'no user with username <b>@{value}</b> in the database — the bot only '
                f'knows people who have used it. send a numeric id instead.'
            )
            return
    else:
        user_id = int(value)
        user = await user_repo.get_user_by_id(user_id) or await user_repo.add_user(user_id=user_id)

    await state.clear()

    if user.is_banned:
        await message.answer(f'{user_label(user)} is already banned.')
    else:
        user = await user_repo.update_user(user.user_id, is_banned=True)
        await message.answer(f'banned {user_label(user)} — <code>{user.user_id}</code>')

    await show_list(message, user_repo, page=0, edit=False)
