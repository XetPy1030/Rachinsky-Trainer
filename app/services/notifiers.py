from app.instances import bot
from app.utils.dt import get_current_dt_for_view
from app.utils.notify import notify_admins


async def notify_about_startup():
    bot_info = await bot.get_me()

    text = (
        "🟢 <b>Бот запущен!</b>\n\n"
        f"🤖 <b>Имя:</b> {bot_info.full_name}\n"
        f"🔗 <b>Username:</b> @{bot_info.username}\n"
        f"🕐 <b>Время запуска:</b> {get_current_dt_for_view()}\n\n"
        "Система готова к работе!"
    )

    await notify_admins(text)
