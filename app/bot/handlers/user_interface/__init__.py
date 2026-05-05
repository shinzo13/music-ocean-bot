from .home import router as home_router
from .user_profile import router as user_profile_router
from .settings.settings import router as user_settings_router
from .settings.language import router as user_settings_language_router
from .settings.scrobbling import router as user_settings_scrobbling_router
from .settings.track_preview import router as user_settings_track_preview_router
from .settings.default_engine import router as user_settings_default_engine_router
from .usage_guide import router as usage_guide_router

routers = [
    home_router,
    user_profile_router,
    user_settings_router,
    user_settings_language_router,
    user_settings_scrobbling_router,
    user_settings_track_preview_router,
    user_settings_default_engine_router,
    usage_guide_router
]