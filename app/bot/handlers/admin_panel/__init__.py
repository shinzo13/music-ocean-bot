from aiogram import Router

from app.bot.filters import IsAdmin

from .admin_panel import router as main_panel_router
from .export_users import router as export_users_router
from .mailing import router as mailing_router
from .ban_user import router as ban_user_router
from .usage_stats import router as usage_stats_router
from .notifications import router as notifications_router

admin_router = Router(name="admin_panel")
admin_router.message.filter(IsAdmin())
admin_router.callback_query.filter(IsAdmin())
admin_router.include_routers(
    ban_user_router, export_users_router, main_panel_router, mailing_router,
    usage_stats_router, notifications_router,
)

routers = [admin_router]
