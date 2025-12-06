"""
Миддлвар для аутентификации
"""
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.services.user import UserService
from app.utils.logger import get_logger
from app.utils.telegram_event import get_author_action_user_from_event

logger = get_logger(__name__)


class AuthMiddleware(BaseMiddleware):
    """Миддлвар для аутентификации и создания пользователей"""

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
            data: Dict[str, Any]) -> Any:
        telegram_user = get_author_action_user_from_event(event)

        if telegram_user:
            if await UserService.is_tg_user_blocked(telegram_user.id):
                logger.warning(f"Заблокированный пользователь {telegram_user.id} пытался использовать бота")
                return

            db_user = await UserService.get_or_create_user(telegram_user)
            data["user"] = db_user
            data["telegram_user"] = telegram_user

            logger.debug(f"Пользователь {telegram_user.id} аутентифицирован")

            await db_user.update_activity()

        else:
            data["user"] = None
            data["telegram_user"] = None

        return await handler(event, data)
