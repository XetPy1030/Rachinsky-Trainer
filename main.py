"""
YouTube Downloader Bot
Главный файл для запуска бота
"""
import asyncio

from dotenv import load_dotenv
from tortoise import Tortoise

from app.config import tortoise_config
from app.instances import dp, bot
from app.middlewares.auth import AuthMiddleware
from app.services.notifiers import notify_about_startup
from app.utils.logger import setup_logger, get_logger

load_dotenv()

setup_logger()
logger = get_logger(__name__)


async def main():
    """Главная функция"""

    logger.info("Запуск Rachinsky Bot...")

    await Tortoise.init(config=tortoise_config)

    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(AuthMiddleware())

    from app.handlers import router
    dp.include_router(router)

    logger.info("Уведомление администраторам о запуск...")
    await notify_about_startup()

    logger.info("Поллинг бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
