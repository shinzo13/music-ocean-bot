import html

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_i18n import I18nContext
from dishka import FromDishka

from app.database.repositories import UserRepository

router = Router()

MEDALS = {1: "🥇", 2: "🥈", 3: "🥉"}


def _name(user) -> str:
    full = " ".join(p for p in (user.first_name, user.last_name) if p)
    return full or (f"@{user.username}" if user.username else str(user.user_id))


@router.message(Command("top"))
async def top_downloaders(message: Message, user_repo: FromDishka[UserRepository], i18n: I18nContext):
    rows = await user_repo.top_users(limit=10)
    if not rows:
        await message.answer(i18n.get('top-empty'))
        return
    lines = [i18n.get('top-title'), ""]
    for i, (user, count) in enumerate(rows, 1):
        rank = MEDALS.get(i, f"{i}.")
        lines.append(f"{rank} {html.escape(_name(user))} — <b>{count}</b>")
    await message.answer("\n".join(lines))
