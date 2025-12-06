"""
Настройка команд бота
"""
from aiogram.types import BotCommand

from app.instances import bot


async def set_bot_commands() -> None:
    """Устанавливает список команд бота"""
    commands = [
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="tasks", description="Начать решать задачи"),
        BotCommand(command="task", description="Задача по номеру /task 42"),
        BotCommand(command="task_random", description="Случайная задача"),
        BotCommand(command="task_stats", description="Моя статистика"),
        BotCommand(command="task_top", description="Топ за сегодня и глобальный"),
        BotCommand(command="task_info", description="Статистика по задаче /task_info 42"),
    ]
    await bot.set_my_commands(commands)

