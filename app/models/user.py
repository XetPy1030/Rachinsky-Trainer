"""
Модель пользователя
"""
from datetime import datetime, UTC

from tortoise import fields
from tortoise.models import Model


class User(Model):
    """Модель пользователя бота"""

    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True, description="Telegram ID пользователя")
    username = fields.CharField(max_length=255, null=True, description="Telegram username")
    first_name = fields.CharField(max_length=255, null=True, description="Имя пользователя")
    last_name = fields.CharField(max_length=255, null=True, description="Фамилия пользователя")
    is_admin = fields.BooleanField(default=False, description="Является ли администратором")
    is_blocked = fields.BooleanField(default=False, description="Заблокирован ли пользователь")
    language_code = fields.CharField(max_length=10, null=True, description="Код языка")

    created_at = fields.DatetimeField(auto_now_add=True, description="Дата регистрации")
    updated_at = fields.DatetimeField(auto_now=True, description="Дата последнего обновления")
    last_activity = fields.DatetimeField(null=True, description="Последняя активность")

    class Meta:
        table = "users"
        table_description = "Пользователи бота"

    def __str__(self) -> str:
        return f"User(telegram_id={self.telegram_id}, username={self.username})"

    async def update_activity(self) -> None:
        """Обновляет время последней активности"""
        from app.utils.dt import get_current_dt
        self.last_activity = get_current_dt()
        await self.save(update_fields=["last_activity"])

    @property
    def full_name(self) -> str:
        """Возвращает полное имя пользователя"""
        parts = []
        if self.first_name:
            parts.append(self.first_name)
        if self.last_name:
            parts.append(self.last_name)
        return " ".join(parts) or self.username or f"User {self.telegram_id}"
