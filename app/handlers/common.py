"""
Общие хендлеры бота
"""
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.models import User
from app.services import TaskProgressService
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = Router()


def _commands_hint() -> str:
    return (
        "Команды:\n"
        "/tasks — начать решать\n"
        "/task номер — задача по номеру (пример: /task 42)\n"
        "/task_random — случайная задача\n"
        "/task_stats — моя статистика\n"
        "/task_top — топ за сегодня и глобальный\n"
        "/task_info номер — статистика по задаче (пример: /task_info 42)\n"
        "/help — показать помощь"
    )


@router.message(CommandStart())
async def start_handler(message: Message, user: User):
    """Обработчик команды /start"""
    today = await TaskProgressService.get_user_today_counts(user)
    accuracy = round((today['correct'] / today['total']) * 100, 1) if today['total'] else 0.0

    welcome_text = (
        "Привет! Я бот для решения задач из списка, можешь решать по порядку, по номеру или брать случайные.\n\n"
        f"За сегодня: верно {today['correct']} из {today['total']} (точность {accuracy}%).\n\n"
        f"{_commands_hint()}"
    )

    await message.answer(welcome_text)
    logger.info(f"Пользователь {user.telegram_id} запустил бота")


@router.message(Command("help"))
async def help_handler(message: Message, user: User):
    """Обработчик команды /help"""
    help_text = (
        "Я даю задачи с ответами. Можно идти по порядку, по номеру или случайно. "
        "Отвечай текстом, можно скипать или сразу смотреть ответ. Вот что доступно:\n\n"
        f"{_commands_hint()}"
    )

    await message.answer(help_text)
