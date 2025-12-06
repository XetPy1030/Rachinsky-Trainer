from app.config import settings
from app.instances import bot
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def notify_admins(text: str):
    for admin_id in settings.admin_ids:
        try:
            await bot.send_message(admin_id, text)
        except Exception as e:
            logger.warning(f"Не удалось уведомить администратора {admin_id}: {e}")
