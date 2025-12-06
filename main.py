"""
YouTube Downloader Bot
Главный файл для запуска бота
"""

from dotenv import load_dotenv

load_dotenv()

import asyncio

from tortoise import Tortoise

from app.config import tortoise_config
from app.instances import dp, bot
from app.utils.logger import setup_logger, get_logger

setup_logger()
logger = get_logger(__name__)


async def main():
    """Главная функция"""

    logger.info("Запуск Rachinsky Bot...")

    await Tortoise.init(config=tortoise_config)

    from app.middlewares.auth import AuthMiddleware
    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(AuthMiddleware())

    from app.handlers import router
    dp.include_router(router)

    from app.services import set_bot_commands
    await set_bot_commands()

    logger.info("Уведомление администраторам о запуск...")
    from app.services import notify_about_startup
    await notify_about_startup()

    logger.info("Поллинг бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
