from aiogram import Router

from . import common

def setup_routers() -> Router:
    router = Router()

    router.include_router(common.router)
    return router

# from .common import router as common_router

# __all__ = ["common_router"]