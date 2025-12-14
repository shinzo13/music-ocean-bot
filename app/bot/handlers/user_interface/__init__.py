from .home import router as home_router
from .user_profile import router as user_profile_router
from .user_settings import router as user_settings_router
from .usage_guide import router as usage_guide_router

routers = [home_router, user_profile_router, user_settings_router, usage_guide_router]