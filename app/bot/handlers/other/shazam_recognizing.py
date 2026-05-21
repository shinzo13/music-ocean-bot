from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from dishka import FromDishka

from app.bot.handlers.user_interface.home import MainMenuCallback, MainMenuPath
from app.bot.keyboards import admin_panel_keyboard
from app.modules.musicocean.enums import Engine
from app.modules.musicocean_tg import TelegramMusicOceanClient

router = Router()


@router.message(F.voice)
async def admin_panel(
        message: Message,
        bot: Bot,
        musicocean: FromDishka[TelegramMusicOceanClient],
        i18n: I18nContext
):
    msg = await message.answer(i18n.get('recognizing'))
    audio = (await bot.download(message.voice.file_id)).read()
    match = await musicocean.shazam_recognize(audio)
    if match:
        await msg.delete()
        cached_track = await musicocean.download_track(Engine.YOUTUBE, match.id)
        await message.answer_audio(cached_track.file_id)
        return

    await msg.edit_text(i18n.get('not-recognized'))
