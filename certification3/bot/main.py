import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from states import AddTaskStates
from keyboards import get_delete_task_keyboard
from datetime import datetime

# Инициализация бота
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())
SERVER_URL = os.getenv("SERVER_URL")

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот для управления задачами.\n"
                         "Команды:\n"
                         "/start - Показать это сообщение\n"
                         "/show_tasks - Показать список задач\n"
                         "/add_task - Добавить новую задачу\n"
                         "/delete_task - Удалить задачу")

# Обработчик команды /show_tasks
@dp.message(Command("show_tasks"))
async def cmd_show_tasks(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{SERVER_URL}/tasks") as response:
            if response.status == 200:
                tasks = await response.json()
                if tasks:
                    tasks_text = "\n".join(
                        f"{task['id']}. {task['name']} (дедлайн: {task['deadline']})"
                        for task in tasks
                    )
                    await message.answer(tasks_text)
                else:
                    await message.answer("Задач нет.")
            else:
                await message.answer("Ошибка при получении задач.")

# Обработчик команды /add_task
@dp.message(Command("add_task"))
async def cmd_add_task(message: types.Message, state: FSMContext):
    await message.answer("Введите название задачи.")
    await state.set_state(AddTaskStates.name)

# Обработчик ввода названия задачи
@dp.message(AddTaskStates.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите дедлайн (ДД.ММ.ГГГГ).")
    await state.set_state(AddTaskStates.deadline)

# Обработчик ввода дедлайна
@dp.message(AddTaskStates.deadline)
async def process_deadline(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data["name"]
    deadline = message.text.strip()  # Удаляем лишние пробелы

    # Валидация формата даты
    try:
        datetime.strptime(deadline, "%d.%m.%Y")
    except ValueError:
        await message.answer("Некорректный формат даты! Пожалуйста, введите дату в формате ДД.ММ.ГГГГ (например, 25.11.2025). Попробуйте снова.")
        return  # Останавливаем выполнение и ждем нового ввода

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{SERVER_URL}/tasks", json={"name": name, "deadline": deadline}) as response:
            if response.status == 200:
                await message.answer("Задача добавлена!")
            else:
                await message.answer("Ошибка при добавлении задачи.")
    await state.clear()

# Обработчик команды /delete_task
@dp.message(Command("delete_task"))
async def cmd_delete_task(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{SERVER_URL}/tasks") as response:
            if response.status == 200:
                tasks = await response.json()
                if tasks:
                    # Формируем текстовый список задач
                    tasks_text = "\n".join(
                        f"{task['id']}. {task['name']} (дедлайн: {task['deadline']})"
                        for task in tasks
                    )
                    # Создаем клавиатуру для удаления
                    keyboard = get_delete_task_keyboard(tasks)
                    await message.answer(f"Список задач:\n{tasks_text}\n\nВыберите задачу для удаления:", reply_markup=keyboard)
                else:
                    await message.answer("Задач нет.")
            else:
                await message.answer("Ошибка при получении задач.")

# Обработчик инлайн-кнопок для удаления
@dp.callback_query(lambda c: c.data.startswith("delete_"))
async def process_delete_callback(callback: types.CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{SERVER_URL}/tasks/{task_id}") as response:
            if response.status == 200:
                await callback.message.edit_text("Задача удалена!")
            else:
                await callback.message.edit_text("Ошибка при удалении задачи.")
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())