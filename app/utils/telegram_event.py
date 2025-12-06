from aiogram.types import TelegramObject, Update


def get_author_action_user_from_event(event: TelegramObject):
    """
    Получение пользователя который совершил действие.

    :param event:
    :return:
    """
    telegram_user = None

    if hasattr(event, 'from_user'):
        telegram_user = event.from_user

    # Если это Update объект
    elif isinstance(event, Update):
        if event.message:
            telegram_user = event.message.from_user
        elif event.callback_query:
            telegram_user = event.callback_query.from_user
        elif event.inline_query:
            telegram_user = event.inline_query.from_user

    return telegram_user
