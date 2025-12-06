"""
Хендлеры бота
"""
from aiogram import Router

from .common import router as common_router
from .tasks import router as tasks_router

router = Router()
router.include_router(common_router)
router.include_router(tasks_router)

__all__ = ["router"]
