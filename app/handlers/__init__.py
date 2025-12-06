"""
Хендлеры бота
"""
from aiogram import Router

from .common import router as common_router

router = Router()
router.include_router(common_router)

__all__ = ["router"]
