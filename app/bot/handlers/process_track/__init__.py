from .inline_chosen import router as process_track_router
from .download_all import router as download_all_router
from .pending_tracks import router as pending_tracks_router

routers = [process_track_router, download_all_router, pending_tracks_router]