"""
Попытки решения задач пользователями
"""
from tortoise import fields
from tortoise.models import Model

from app.models.user import User


class TaskAttempt(Model):
    """Результат решения одной задачи пользователем"""

    id = fields.IntField(pk=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User",
        related_name="task_attempts",
        on_delete=fields.CASCADE,
        description="Пользователь",
    )
    task_number = fields.IntField(description="Номер задачи из файла")
    user_answer = fields.TextField(null=True, description="Ответ пользователя (если был)")
    status = fields.CharField(max_length=16, description="Статус: correct/incorrect/skipped")
    is_correct = fields.BooleanField(null=True, description="Верно ли (None для skip)")
    created_at = fields.DatetimeField(auto_now_add=True, description="Когда отвечено")

    class Meta:
        table = "task_attempts"
        table_description = "История решений задач"
        unique_together = (("user", "task_number"),)

    def __str__(self) -> str:
        return f"TaskAttempt(user={self.user_id}, task={self.task_number}, status={self.status})"

