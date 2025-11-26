from aiogram import Router, F, Bot
from aiogram.types import ChosenInlineResult
from aiogram.types import InputMediaAudio
from dishka import FromDishka

from app.modules.musicocean_tg import TelegramMusicOceanClient

router = Router()



@router.chosen_inline_result()
async def idklol(
        chosen: ChosenInlineResult,
        bot: Bot,
        musicocean: FromDishka[TelegramMusicOceanClient]
):
    file_id = await musicocean.download_track(track_id=int(chosen.result_id))
    await bot.edit_message_media(
        media=InputMediaAudio(media=file_id),
        inline_message_id=chosen.inline_message_id
    )
