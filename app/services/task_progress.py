"""
Сервис для записи результатов решения задач
"""
from typing import Optional

from app.models import TaskAttempt, User
from app.services.tasks import Task
from app.utils.logger import get_logger

logger = get_logger(__name__)


class TaskProgressService:
    """Работа с результатами задач"""

    STATUS_CORRECT = "correct"
    STATUS_INCORRECT = "incorrect"
    STATUS_SKIPPED = "skipped"

    @classmethod
    async def log_attempt(
        cls,
        *,
        user: User,
        task: Task,
        status: str,
        user_answer: Optional[str] = None,
        is_correct: Optional[bool] = None,
    ) -> TaskAttempt:
        """Создает или обновляет запись о попытке решения"""
        attempt = await TaskAttempt.get_or_none(user=user, task_number=task.number)
        if attempt:
            attempt.status = status
            attempt.user_answer = user_answer
            attempt.is_correct = is_correct
            await attempt.save(update_fields=["status", "user_answer", "is_correct"])
            logger.debug(
                "Обновлена попытка задачи",
                user_id=user.id,
                task_number=task.number,
                status=status,
                is_correct=is_correct,
            )
            return attempt

        attempt = await TaskAttempt.create(
            user=user,
            task_number=task.number,
            user_answer=user_answer,
            status=status,
            is_correct=is_correct,
        )
        logger.debug(
            "Создана попытка задачи",
            user_id=user.id,
            task_number=task.number,
            status=status,
            is_correct=is_correct,
        )
        return attempt

    @staticmethod
    async def get_last_task_number(user: User) -> int:
        """Возвращает номер последней решённой или пропущенной задачи для пользователя"""
        last_attempt = (
            await TaskAttempt.filter(user=user)
            .order_by("-task_number")
            .first()
        )
        return last_attempt.task_number if last_attempt else 0

