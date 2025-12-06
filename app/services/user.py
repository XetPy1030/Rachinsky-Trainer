"""
Сервис для работы с пользователями
"""
from typing import Optional, List
from datetime import datetime, timedelta, UTC
from aiogram.types import User as TelegramUser
from tortoise.queryset import Q
from tortoise.exceptions import DoesNotExist

from app.models import User
from app.config import settings
from app.utils.dt import get_current_dt
from app.utils.logger import get_logger

logger = get_logger(__name__)


class UserService:
    """Сервис для работы с пользователями"""

    @staticmethod
    async def get_or_create_user(
        telegram_user: TelegramUser,
    ) -> User:
        """Получает или создает пользователя"""
        try:
            user = await User.get(telegram_id=telegram_user.id)

            updated = False
            if user.username != telegram_user.username:
                user.username = telegram_user.username
                updated = True
            if user.first_name != telegram_user.first_name:
                user.first_name = telegram_user.first_name
                updated = True
            if user.last_name != telegram_user.last_name:
                user.last_name = telegram_user.last_name
                updated = True
            if user.language_code != telegram_user.language_code:
                user.language_code = telegram_user.language_code
                updated = True

            if updated:
                await user.save()

        except DoesNotExist:
            # Создаем нового пользователя
            is_admin = telegram_user.id in settings.admin_ids

            user = await User.create(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name,
                language_code=telegram_user.language_code,
                is_admin=is_admin,
                last_activity=get_current_dt()
            )

            logger.info(f"Создан новый пользователь: {user}")

        return user

    @staticmethod
    async def is_tg_user_blocked(telegram_id: int) -> bool:
        """Проверяет, заблокирован ли пользователь"""
        try:
            user = await User.get(telegram_id=telegram_id)
            return user.is_blocked
        except DoesNotExist:
            return False

    @staticmethod
    async def block_tg_user(telegram_id: int) -> bool:
        """Блокирует пользователя"""
        try:
            user = await User.get(telegram_id=telegram_id)
            user.is_blocked = True
            await user.save()
            logger.info(f"Пользователь {telegram_id} заблокирован")
            return True
        except DoesNotExist:
            return False

    @staticmethod
    async def unblock_tg_user(telegram_id: int) -> bool:
        """Разблокирует пользователя"""
        try:
            user = await User.get(telegram_id=telegram_id)
            user.is_blocked = False
            await user.save()
            logger.info(f"Пользователь {telegram_id} разблокирован")
            return True
        except DoesNotExist:
            return False

    @staticmethod
    async def get_all_users(
            limit: int = 100,
            offset: int = 0,
            search: str = None
    ) -> List[User]:
        """Получает список всех пользователей"""
        query = User.all()

        if search:
            query = query.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )

        return await query.offset(offset).limit(limit).order_by("-created_at")

    @staticmethod
    async def get_admin_users() -> List[User]:
        """Получает список администраторов"""
        return await User.filter(is_admin=True)

    @staticmethod
    async def promote_to_admin(telegram_id: int) -> bool:
        """Делает пользователя администратором"""
        try:
            user = await User.get(telegram_id=telegram_id)
            user.is_admin = True
            await user.save()
            logger.info(f"Пользователь {telegram_id} повышен до администратора")
            return True
        except DoesNotExist:
            return False

    @staticmethod
    async def demote_from_admin(telegram_id: int) -> bool:
        """Снимает права администратора"""
        try:
            user = await User.get(telegram_id=telegram_id)
            user.is_admin = False
            await user.save()
            logger.info(f"У пользователя {telegram_id} сняты права администратора")
            return True
        except DoesNotExist:
            return False

    @staticmethod
    async def get_users_count() -> int:
        """Получает общее количество пользователей"""
        return await User.all().count()
