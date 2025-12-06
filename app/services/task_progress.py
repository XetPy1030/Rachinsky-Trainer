"""
Сервис для записи результатов решения задач и статистики
"""
from typing import Optional, List

from tortoise.functions import Count

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

    @staticmethod
    async def get_user_stats(user: User) -> dict:
        """Персональная статистика пользователя"""
        total = await TaskAttempt.filter(user=user).count()
        correct = await TaskAttempt.filter(user=user, status=TaskProgressService.STATUS_CORRECT).count()
        incorrect = await TaskAttempt.filter(user=user, status=TaskProgressService.STATUS_INCORRECT).count()
        skipped = await TaskAttempt.filter(user=user, status=TaskProgressService.STATUS_SKIPPED).count()

        accuracy = round((correct / total) * 100, 1) if total else 0.0

        return {
            "total": total,
            "correct": correct,
            "incorrect": incorrect,
            "skipped": skipped,
            "accuracy": accuracy,
        }

    @staticmethod
    async def get_leaderboard(limit: int = 10) -> List[dict]:
        """Глобальный топ по числу верных задач"""
        rows = (
            await TaskAttempt.filter(status=TaskProgressService.STATUS_CORRECT)
            .annotate(correct_count=Count("id"))
            .group_by("user_id")
            .order_by("-correct_count")
            .limit(limit)
            .values("user_id", "correct_count")
        )
        user_ids = [row["user_id"] for row in rows]
        users = await User.filter(id__in=user_ids)
        users_map = {u.id: u for u in users}

        leaderboard = []
        for idx, row in enumerate(rows, start=1):
            user = users_map.get(row["user_id"])
            leaderboard.append(
                {
                    "place": idx,
                    "user": user,
                    "correct": row["correct_count"],
                }
            )
        return leaderboard

    @staticmethod
    async def get_task_stats(task_number: int) -> dict:
        """Статистика по конкретной задаче"""
        total = await TaskAttempt.filter(task_number=task_number).count()
        correct = await TaskAttempt.filter(
            task_number=task_number,
            status=TaskProgressService.STATUS_CORRECT
        ).count()
        incorrect = await TaskAttempt.filter(
            task_number=task_number,
            status=TaskProgressService.STATUS_INCORRECT
        ).count()
        skipped = await TaskAttempt.filter(
            task_number=task_number,
            status=TaskProgressService.STATUS_SKIPPED
        ).count()
        accuracy = round((correct / total) * 100, 1) if total else 0.0

        return {
            "total": total,
            "correct": correct,
            "incorrect": incorrect,
            "skipped": skipped,
            "accuracy": accuracy,
        }
