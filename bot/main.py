import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from states import AddTaskStates
from keyboards import get_delete_task_keyboard, get_cancel_keyboard
from datetime import datetime

# Инициализация бота
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())
SERVER_URL = os.getenv("SERVER_URL")

# Обработка команд
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот для управления задачами.\n"
        "Команды:\n"
        "/start - Показать это сообщение\n"
        "/show_tasks - Показать список задач\n"
        "/add_task - Добавить новую задачу\n"
        "/delete_task - Удалить задачу",
    )

@dp.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Действие отменено.",
    )

# Обработка задач
@dp.message(Command("show_tasks"))
async def cmd_show_tasks(message: types.Message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{SERVER_URL}/tasks?user_id={message.from_user.id}"
            ) as response:
                if response.status == 200:
                    tasks = await response.json()
                    if tasks:
                        tasks_text = "\n".join(
                            f"{task['id']}. {task['name']} (дедлайн: {task['deadline']})"
                            for task in tasks
                        )
                        await message.answer(
                            f"Ваши задачи:\n{tasks_text}"
                        )
                    else:
                        await message.answer(
                            "Задач нет."
                        )
                else:
                    error = await response.text()
                    await message.answer(
                        f"❌ Ошибка при получении задач: {error}",
                    )
    except Exception as e:
        await message.answer(
            f"⚠️ Ошибка подключения: {str(e)}"
        )

# Добавление задачи
@dp.message(Command("add_task"))
async def cmd_add_task(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Введите название задачи:",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(AddTaskStates.name)

@dp.message(AddTaskStates.name)
async def process_name(message: types.Message, state: FSMContext):
    if message.text.startswith('/'):
        await dp.feed_update(bot, types.Update(
            update_id=0,
            message=message
        ))
        return
    
    await state.update_data(name=message.text)
    await message.answer(
        "Введите дедлайн (ДД.ММ.ГГГГ):",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(AddTaskStates.deadline)

@dp.message(AddTaskStates.deadline)
async def process_deadline(message: types.Message, state: FSMContext):
    user_input = message.text.strip()
    
    # Обработка команды отмены
    if user_input.lower() == "/cancel":
        await state.clear()
        await message.answer(
            "❌ Добавление задачи отменено",
            reply_markup=get_main_menu_keyboard()
        )
        return
    
    try:
        # Получаем сохраненные данные
        data = await state.get_data()
        name = data["name"]
        user_id = message.from_user.id
        
        # Парсим дату
        deadline_date = datetime.strptime(user_input, "%d.%m.%Y").date()
        today = datetime.now().date()
        
        # Проверяем что дата в будущем
        if deadline_date < today:
            await message.answer(
                f"📅 Дата должна быть не раньше сегодняшнего дня ({today.strftime('%d.%m.%Y')})!\n"
                "Пожалуйста, введите новую дату (ДД.ММ.ГГГГ):",
                reply_markup=get_cancel_keyboard()
            )
            # Сохраняем имя задачи для повторного использования
            await state.update_data(name=name)
            return
        
        # Отправляем данные на сервер
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                f"{SERVER_URL}/tasks",
                json={
                    "name": name,
                    "deadline": deadline_date.strftime("%Y-%m-%d"),
                    "user_id": user_id
                }
            )
            
            if response.status == 200:
                await message.answer(
                    f"✅ Задача '{name}' успешно добавлена!\n"
                    f"Дедлайн: {user_input}",
                )
                await state.clear()
            else:
                error = await response.text()
                await message.answer(
                    f"❌ Ошибка сервера: {error}\n"
                    "Попробуйте ввести дату снова:",
                    reply_markup=get_cancel_keyboard()
                )
                # Сохраняем данные для повторной попытки
                await state.set_state(AddTaskStates.deadline)
                await state.update_data(name=name)
    
    except ValueError:
        await message.answer(
            "❌ Неверный формат даты! Требуется ДД.ММ.ГГГГ\n"
            "Пример: 15.07.2025\n"
            "Пожалуйста, введите дату заново:",
            reply_markup=get_cancel_keyboard()
        )
        await state.set_state(AddTaskStates.deadline)
        await state.update_data(name=data["name"])


# Удаление задачи
@dp.message(Command("delete_task"))
async def cmd_delete_task(message: types.Message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{SERVER_URL}/tasks?user_id={message.from_user.id}"
            ) as response:
                if response.status == 200:
                    tasks = await response.json()
                    if tasks:
                        await message.answer(
                            "Выберите задачу для удаления:",
                            reply_markup=get_delete_task_keyboard(tasks)
                        )
                    else:
                        await message.answer(
                            "❗ Нет задач для удаления",
                        )
                else:
                    error = await response.text()
                    await message.answer(
                        f"❌ Ошибка: {error}",
                    )
    except Exception as e:
        await message.answer(
            f"⚠️ Ошибка подключения: {str(e)}",
        )

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
                        "✅ Задача удалена!",
                        reply_markup=None
                    )
                else:
                    error = await response.text()
                    await callback.message.edit_text(
                        f"❌ Ошибка: {error}",
                        reply_markup=None
                    )
    except Exception as e:
        await callback.message.edit_text(
            f"⚠️ Ошибка подключения: {str(e)}",
            reply_markup=None
        )
    await callback.answer()

# Обработка сообщений
@dp.message(F.content_type.in_({'photo', 'video', 'document', 'sticker'}))
async def handle_media(message: types.Message):
    await message.answer(
        "📎 Я работаю только с текстовыми командами.",
    )

@dp.message(F.text.lower().in_({"меню", "старт", "start", "команды"}))
async def handle_text_commands(message: types.Message):
    await cmd_start(message)

@dp.message()
async def handle_other_messages(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
        await message.answer(
            "Пожалуйста, используйте команды из меню.",
        )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())