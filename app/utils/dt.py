from datetime import datetime, UTC

from app.instances import current_timezone


def get_current_dt_for_view() -> str:
    return (
        get_current_dt().astimezone(current_timezone).strftime('%d.%m.%Y %H:%M:%S')
    )


def get_current_dt() -> datetime:
    return datetime.now(UTC)
