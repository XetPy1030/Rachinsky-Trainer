from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from pytz import timezone
from redis.asyncio import Redis

from app.config import settings

bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

redis = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password,
    db=settings.redis_db,
)

storage = RedisStorage(
    redis=redis,
)

dp = Dispatcher(storage=storage)

current_timezone = timezone(settings.timezone)
