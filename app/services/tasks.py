"""
Сервис для работы с задачами из файла tasks.txt
"""
from dataclasses import dataclass
from pathlib import Path
from random import choice
import re
from typing import List, Optional

from app.config import app_path
from app.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True, slots=True)
class Task:
    """Модель задачи, извлечённой из файла"""

    number: int
    description: str
    answer: str


class TaskService:
    """Сервис для загрузки и поиска задач"""

    _tasks_cache: List[Task] | None = None
    _tasks_by_number: dict[int, Task] | None = None

    # Ожидаемый формат строки: "1. Описание [ответ]"
    _pattern = re.compile(r"^\s*(\d+)\.\s*(.+?)\s*\[(.+?)\]\s*$")

    @classmethod
    def _parse_line(cls, line: str) -> Optional[Task]:
        """Парсит одну строку задачи, возвращает None если формат не распознан"""
        match = cls._pattern.match(line.strip())
        if not match:
            logger.warning("Не удалось распарсить строку с задачей", line=line)
            return None

        number, description, answer = match.groups()
        return Task(
            number=int(number),
            description=description.strip(),
            answer=answer.strip(),
        )

    @classmethod
    def _load_tasks(cls, tasks_path: Optional[Path] = None) -> List[Task]:
        """Загружает и кэширует задачи из файла"""
        path = tasks_path or (app_path / "tasks.txt")
        try:
            text = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            logger.error("Файл с задачами не найден", path=str(path))
            cls._tasks_cache = []
            cls._tasks_by_number = {}
            return []

        tasks: List[Task] = []
        for raw_line in text.splitlines():
            if not raw_line.strip():
                continue

            task = cls._parse_line(raw_line)
            if task:
                tasks.append(task)

        tasks.sort(key=lambda t: t.number)
        cls._tasks_cache = tasks
        cls._tasks_by_number = {task.number: task for task in tasks}

        logger.info(f"Загружено задач: {len(tasks)}")
        return tasks

    @classmethod
    def get_all_tasks(cls, *, force_reload: bool = False) -> List[Task]:
        """Возвращает все задачи, при необходимости перечитывает файл"""
        if force_reload or cls._tasks_cache is None:
            return cls._load_tasks()
        return cls._tasks_cache

    @classmethod
    def get_task_by_number(cls, number: int) -> Optional[Task]:
        """Возвращает задачу по её номеру"""
        if cls._tasks_by_number is None:
            cls._load_tasks()
        return cls._tasks_by_number.get(number) if cls._tasks_by_number else None

    @classmethod
    def get_random_task(cls) -> Optional[Task]:
        """Возвращает случайную задачу"""
        tasks = cls.get_all_tasks()
        if not tasks:
            return None
        return choice(tasks)

    @classmethod
    def search_tasks(cls, query: str, *, limit: int = 10) -> List[Task]:
        """Простой полнотекстовый поиск по описанию"""
        if not query:
            return []

        q = query.lower()
        results = [task for task in cls.get_all_tasks() if q in task.description.lower()]
        return results[:limit]

    @classmethod
    def slice_tasks(cls, offset: int = 0, limit: int = 20) -> List[Task]:
        """Получает часть списка задач для пагинации"""
        tasks = cls.get_all_tasks()
        return tasks[offset: offset + limit]

