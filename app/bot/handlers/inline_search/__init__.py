from .link_search import router as link_search_router
from .advanced_search import router as advanced_search_router
from .id_search import router as id_search_router
from .default_search import router as default_search_router
from .empty_search import router as empty_search_router
routers = [
    link_search_router,
    advanced_search_router,
    id_search_router,
    default_search_router,
    empty_search_router,
]