from .track_entity import router as track_entity_router
from .track_info_ready import router as track_info_ready_router

routers = [track_info_ready_router, track_entity_router]
