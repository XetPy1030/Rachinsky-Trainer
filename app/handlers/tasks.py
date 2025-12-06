"""
Хендлеры для решения задач
"""
import re

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
    """Упрощённая нормализация ответа для сравнения"""
    cleaned = re.sub(r"[^\w\s.,-]", "", text.strip().lower())
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def _task_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏭️ Скип", callback_data="task_skip")],
        ]
    )


async def _send_task(target_message: Message, state: FSMContext, task: Task) -> None:
    """Отправляет задачу и ставит состояние ожидания ответа"""
    await state.set_state(TaskSolveState.waiting_answer)
    await state.update_data(current_task_number=task.number)

    text = (
        f"Задача #{task.number}\n"
        f"{task.description}\n\n"
        "Отправь ответ сообщением или нажми «Скип»."
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

