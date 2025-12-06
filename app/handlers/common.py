"""
Общие хендлеры бота
"""
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.models import User
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, user: User):
    """Обработчик команды /start"""

    welcome_text = f"""
Мне впадлу думать что здесь будет заранее.
    """

    await message.answer(welcome_text, )

    logger.info(f"Пользователь {user.telegram_id} запустил бота")


@router.message(Command("help"))
async def help_handler(message: Message, user: User):
    """Обработчик команды /help"""

    help_text = """
Хелпа
    """

    await message.answer(help_text)
