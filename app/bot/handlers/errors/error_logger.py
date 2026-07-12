from aiogram import Router
from aiogram.types import ErrorEvent

from app.config.log import get_logger

logger = get_logger(__name__)

router = Router()


@router.errors()
async def log_error(event: ErrorEvent):
    update = event.update
    ctx = "?"
    if update.message:
        m = update.message
        ctx = f"message chat={m.chat.id} from={m.from_user.id if m.from_user else None} sender_chat={m.sender_chat.id if m.sender_chat else None}"
    elif update.inline_query:
        ctx = f"inline_query from={update.inline_query.from_user.id} q={update.inline_query.query!r}"
    elif update.chosen_inline_result:
        c = update.chosen_inline_result
        ctx = f"chosen_inline_result from={c.from_user.id} result_id={c.result_id} inline_message_id={c.inline_message_id}"
    elif update.callback_query:
        ctx = f"callback_query from={update.callback_query.from_user.id} data={update.callback_query.data!r}"
    logger.exception(f"unhandled error on {update.event_type} [{ctx}]: {event.exception}")
    return True
