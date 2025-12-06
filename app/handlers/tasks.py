"""
Хендлеры для решения задач
"""
import re
from decimal import Decimal, InvalidOperation

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from app.models import User
from app.services import TaskService, TaskProgressService, Task
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = Router()


class TaskSolveState(StatesGroup):
    waiting_answer = State()


def _normalize_answer(text: str) -> str:
    """Гибкая нормализация: регистр, пробелы, знаки, числа с . или ,"""
    if not text:
        return ""

    lowered = text.strip().lower().replace(",", ".")
    cleaned = re.sub(r"[^\w\s.\-]", " ", lowered)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    numeric_candidate = cleaned.replace(" ", "")
    try:
        dec = Decimal(numeric_candidate)
        dec = dec.normalize()
        normalized_num = format(dec, "f").rstrip("0").rstrip(".")
        return normalized_num
    except InvalidOperation:
        return cleaned


def _task_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⏭️ Скип", callback_data="task_skip"),
                InlineKeyboardButton(text="👀 Показать ответ", callback_data="task_show_answer"),
            ],
        ]
    )


async def _send_task(target_message: Message, state: FSMContext, task: Task) -> None:
    """Отправляет задачу и ставит состояние ожидания ответа"""
    await state.set_state(TaskSolveState.waiting_answer)
    await state.update_data(current_task_number=task.number)

    text = (
        f"Задача #{task.number}\n"
        f"{task.description}\n\n"
        "Отправь ответ сообщением, нажми «Показать ответ» или «Скип»."
    )
    await target_message.answer(text, reply_markup=_task_keyboard())


def _get_next_task(current_number: int) -> Task | None:
    """Берёт следующую задачу по номеру"""
    return TaskService.get_task_by_number(current_number + 1)


@router.message(Command("tasks"))
async def start_tasks(message: Message, state: FSMContext, user: User):
    """Старт решения задач"""
    last_number = await TaskProgressService.get_last_task_number(user)
    next_number = last_number + 1

    task = TaskService.get_task_by_number(next_number)
    if not task:
        await message.answer("Задачи закончились или не найдены.")
        await state.clear()
        return

    await _send_task(message, state, task)


@router.message(Command("task"))
async def task_by_number(message: Message, state: FSMContext, user: User):
    """Показать задачу по номеру"""
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip().isdigit():
        await message.answer("Укажи номер: /task 42")
        return

    number = int(parts[1].strip())
    task = TaskService.get_task_by_number(number)
    if not task:
        await message.answer("Такой задачи нет.")
        await state.clear()
        return

    await _send_task(message, state, task)


@router.message(Command("task_random"))
async def task_random(message: Message, state: FSMContext, user: User):
    """Показать случайную задачу"""
    task = TaskService.get_random_task()
    if not task:
        await message.answer("Задачи не найдены.")
        await state.clear()
        return

    await _send_task(message, state, task)


@router.message(Command("task_stats"))
async def task_stats(message: Message, user: User):
    """Персональная статистика"""
    stats = await TaskProgressService.get_user_stats(user)
    text = (
        "Твоя статистика:\n"
        f"Всего попыток: {stats['total']}\n"
        f"Верно: {stats['correct']}\n"
        f"Неверно: {stats['incorrect']}\n"
        f"Скип: {stats['skipped']}\n"
        f"Точность: {stats['accuracy']}%"
    )
    await message.answer(text)


@router.message(Command("task_top"))
async def task_top(message: Message):
    """Топы: за сегодня и за всё время"""
    leaders_today = await TaskProgressService.get_leaderboard_today()
    leaders_all = await TaskProgressService.get_leaderboard()

    parts = []

    # Топ за сегодня
    if leaders_today:
        lines = ["🏆 Топ за сегодня:"]
        for row in leaders_today:
            user = row["user"]
            name = user.full_name or user.username or f"ID {user.telegram_id}" if user else "неизвестно"
            lines.append(f"{row['place']}. {name} — {row['correct']} верных")
        parts.append("\n".join(lines))
    else:
        parts.append("🏆 Топ за сегодня:\nПока никто не решил ни одной задачи.")

    # Глобальный топ
    if leaders_all:
        lines = ["🌍 Глобальный топ:"]
        for row in leaders_all:
            user = row["user"]
            name = user.full_name or user.username or f"ID {user.telegram_id}" if user else "неизвестно"
            lines.append(f"{row['place']}. {name} — {row['correct']} верных")
        parts.append("\n".join(lines))
    else:
        parts.append("🌍 Глобальный топ:\nПока нет решённых задач.")

    await message.answer("\n\n".join(parts))


@router.message(Command("task_info"))
async def task_info(message: Message):
    """Статистика по задаче"""
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip().isdigit():
        await message.answer("Укажи номер: /task_info 42")
        return

    number = int(parts[1].strip())
    stats = await TaskProgressService.get_task_stats(number)
    if stats["total"] == 0:
        await message.answer("По этой задаче пока нет попыток.")
        return

    text = (
        f"Статистика по задаче #{number}:\n"
        f"Всего попыток: {stats['total']}\n"
        f"Верно: {stats['correct']}\n"
        f"Неверно: {stats['incorrect']}\n"
        f"Скип: {stats['skipped']}\n"
        f"Точность: {stats['accuracy']}%"
    )
    await message.answer(text)


@router.message(TaskSolveState.waiting_answer)
async def handle_answer(message: Message, state: FSMContext, user: User):
    """Обрабатывает ответ на текущую задачу"""
    data = await state.get_data()
    current_number = data.get("current_task_number")

    if not current_number:
        await message.answer("Нет активной задачи. Отправь /tasks чтобы начать.")
        await state.clear()
        return

    task = TaskService.get_task_by_number(int(current_number))
    if not task:
        await message.answer("Текущая задача не найдена. Попробуй начать заново: /tasks")
        await state.clear()
        return

    if not message.text:
        await message.answer("Пришли ответ текстом.")
        return

    user_answer = message.text.strip()
    is_correct = _normalize_answer(user_answer) == _normalize_answer(task.answer)
    status = TaskProgressService.STATUS_CORRECT if is_correct else TaskProgressService.STATUS_INCORRECT

    await TaskProgressService.log_attempt(
        user=user,
        task=task,
        status=status,
        user_answer=user_answer,
        is_correct=is_correct,
    )

    if is_correct:
        await message.answer("✅ Верно!")
    else:
        await message.answer(f"❌ Неверно. Правильный ответ: {task.answer}")

    next_task = _get_next_task(task.number)
    if not next_task:
        await message.answer("Больше задач нет. Молодец!")
        await state.clear()
        return

    await _send_task(message, state, next_task)


@router.callback_query(TaskSolveState.waiting_answer, F.data == "task_skip")
async def skip_task(callback: CallbackQuery, state: FSMContext, user: User):
    """Пропустить текущую задачу"""
    data = await state.get_data()
    current_number = data.get("current_task_number")

    if not current_number:
        await callback.answer("Нет активной задачи", show_alert=True)
        await state.clear()
        return

    task = TaskService.get_task_by_number(int(current_number))
    if not task:
        await callback.answer("Задача не найдена", show_alert=True)
        await state.clear()
        return

    await TaskProgressService.log_attempt(
        user=user,
        task=task,
        status=TaskProgressService.STATUS_SKIPPED,
        user_answer=None,
        is_correct=None,
    )

    await callback.answer("Пропущена")
    await callback.message.answer(f"Задача #{task.number} пропущена.")

    next_task = _get_next_task(task.number)
    if not next_task:
        await callback.message.answer("Больше задач нет. Возвращайся позже.")
        await state.clear()
        return

    await _send_task(callback.message, state, next_task)


@router.callback_query(TaskSolveState.waiting_answer, F.data == "task_show_answer")
async def show_answer(callback: CallbackQuery, state: FSMContext, user: User):
    """Показать ответ и перейти дальше (считается как неверный)"""
    data = await state.get_data()
    current_number = data.get("current_task_number")

    if not current_number:
        await callback.answer("Нет активной задачи", show_alert=True)
        await state.clear()
        return

    task = TaskService.get_task_by_number(int(current_number))
    if not task:
        await callback.answer("Задача не найдена", show_alert=True)
        await state.clear()
        return

    await TaskProgressService.log_attempt(
        user=user,
        task=task,
        status=TaskProgressService.STATUS_INCORRECT,
        user_answer="(показан ответ)",
        is_correct=False,
    )

    await callback.answer("Ответ показан")
    await callback.message.answer(f"Ответ на задачу #{task.number}: {task.answer}")

    next_task = _get_next_task(task.number)
    if not next_task:
        await callback.message.answer("Больше задач нет. Возвращайся позже.")
        await state.clear()
        return

    await _send_task(callback.message, state, next_task)

