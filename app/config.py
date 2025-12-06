"""
Настройки приложения
"""
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""

    bot_token: str = Field(..., description="Токен Telegram бота")
    admin_ids: list[int] = Field(default_factory=list, description="ID администраторов")

    timezone: str = Field(default="Europe/Moscow", description="TZ для показаний")

    # Database settings
    database_host: str = Field(
        default="localhost",
        description="Хост базы данных"
    )
    database_port: int = Field(
        default=5432,
        description="Порт базы данных"
    )
    database_name: str = Field(
        default="db",
        description="Имя базы данных"
    )
    database_user: str = Field(
        default="user",
        description="Имя пользователя базы данных"
    )
    database_password: str = Field(
        default="password",
        description="Пароль пользователя базы данных"
    )

    # Redis settings
    redis_host: str = Field(
        default="localhost",
        description="Хост Redis"
    )
    redis_port: int = Field(
        default=6379,
        description="Порт Redis"
    )
    redis_db: int = Field(
        default=0,
        description="Номер базы данных Redis"
    )
    redis_password: str = Field(
        default="",
        description="Пароль Redis"
    )

    log_level: str = Field(default="INFO", description="Уровень логирования")
    log_path_file: str = Field(default="app.log", description="Файл логов")

    @field_validator('admin_ids', mode='before')
    @classmethod
    def parse_admin_ids(cls, value: str | int | list[int]) -> list[int]:
        """Парсинг ID администраторов из строки или числа в список"""
        if isinstance(value, str):
            return [int(x.strip()) for x in value.split(',') if x.strip().isdigit()]
        elif isinstance(value, int):
            return [value]
        elif isinstance(value, list):
            return value
        else:
            return []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Игнорировать неизвестные переменные из .env
    
    @property
    def database_url(self) -> str:
        """URL подключения к базе данных"""
        return f"postgres://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"

    @property
    def redis_url(self) -> str:
        """URL подключения к Redis"""
        return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"


settings = Settings()

tortoise_config = {
    "connections": {
        "default": settings.database_url
    },
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        }
    },
    "use_tz": True,
    "timezone": "UTC"
}

app_path = Path(__file__).parent.parent
