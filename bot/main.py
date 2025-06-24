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
    user_id = message.from_user.id
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{SERVER_URL}/tasks?user_id={message.from_user.id}") as response:
            if response.status == 200:
                tasks = await response.json()
                if tasks:
                    tasks_text = "\n".join(
                        f"{task['id']}. {task['name']} (дедлайн: {task['deadline']})"
                        for task in tasks
                    )
                    await message.answer(f"Ваши задачи:\n{tasks_text}")
                else:
                    await message.answer("Задач нет.")
            else:
                await message.answer("❌Ошибка при получении задач.")

@dp.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Действие отменено. Вы можете использовать другие команды.")

# Модифицируем обработчик команды /add_task
@dp.message(Command("add_task"))
async def cmd_add_task(message: types.Message, state: FSMContext):
    await state.clear()  # Очищаем предыдущее состояние
    await message.answer("Введите название задачи (или /cancel для отмены).")
    await state.set_state(AddTaskStates.name)

# Модифицируем обработчик ввода названия задачи
@dp.message(AddTaskStates.name)
async def process_name(message: types.Message, state: FSMContext):
    if message.text.startswith('/'):  # Если введена команда
        await state.clear()  # Очищаем состояние
        await dp.feed_update(bot, types.Update(update_id=0, message=message))  # Обрабатываем команду
        return
    
    await state.update_data(name=message.text)
    await message.answer("Введите дедлайн (ДД.ММ.ГГГГ) или /cancel для отмены.")
    await state.set_state(AddTaskStates.deadline)

# Обработчик ввода дедлайна
@dp.message(AddTaskStates.deadline)
async def process_deadline(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data["name"]
    deadline = message.text.strip()
    user_id = message.from_user.id

    # Валидация формата даты
    try:
        datetime.strptime(deadline, "%d.%m.%Y")
    except ValueError:
        await message.answer("❌Некорректный формат даты! Пожалуйста, введите дату в формате ДД.ММ.ГГГГ (например, 25.11.2025). Попробуйте снова.")
        return  # Останавливаем выполнение и ждем нового ввода

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{SERVER_URL}/tasks",
        json={"name": name, "deadline": deadline, "user_id": user_id}) as response:
            if response.status == 200:
                await message.answer("✅Задача добавлена!")
            else:
                await message.answer("❌Ошибка при добавлении задачи.")
    await state.clear()

@dp.message(Command("delete_task"))
async def cmd_delete_task(message: types.Message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{SERVER_URL}/tasks?user_id={message.from_user.id}") as response:
                if response.status == 200:
                    tasks = await response.json()
                    if tasks:
                        keyboard = get_delete_task_keyboard(tasks)
                        await message.answer(
                            "Выберите задачу для удаления:",
                            reply_markup=keyboard
                        )
                    else:
                        await message.answer("❗ У вас нет задач для удаления")
                else:
                    error = await response.text()
                    await message.answer(f"❌ Ошибка сервера: {error}")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка подключения: {str(e)}")

@dp.callback_query(lambda c: c.data.startswith("delete_"))
async def process_delete_callback(callback: types.CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f"{SERVER_URL}/tasks/{task_id}",
                params={"user_id": user_id}
            ) as response:
                if response.status == 200:
                    await callback.message.edit_text(
                        "✅ Задача успешно удалена!",
                        reply_markup=None
                    )
                else:
                    error = await response.text()
                    await callback.message.edit_text(
                        f"❌ Ошибка удаления: {error}",
                        reply_markup=None
                    )
    except Exception as e:
        await callback.message.edit_text(
            f"⚠️ Ошибка подключения: {str(e)}",
            reply_markup=None
        )
    
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())