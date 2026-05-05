from .admin_panel import router as main_panel_router
from .export_users import router as export_users_router
from .mailing import router as mailing_router

routers = [export_users_router, main_panel_router, mailing_router]
