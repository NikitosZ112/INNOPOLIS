import logging
from aiogram import Bot, types, F
from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import TOKEN, DB_CONFIG
from database import Database

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
db = Database()

class NoteStates(StatesGroup):
    start = State()
    add_note = State()
    delete_note = State()

def get_main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить заметку", callback_data="add_note")],
            [InlineKeyboardButton(text="👀 Просмотреть заметки", callback_data="view_notes")],
            [InlineKeyboardButton(text="❌ Удалить заметку", callback_data="delete_note")]
        ]
    )

def get_delete_menu(notes):
    buttons = []
    for note in notes:
        buttons.append([InlineKeyboardButton(
            text=f"🗑️ {note['note_text'][:30]}",
            callback_data=f"delete_{note['id']}"
        )])
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(NoteStates.start)
    await message.answer(
        "📝 Добро пожаловать в бот для управления заметками!",
        reply_markup=get_main_menu()
    )

@dp.callback_query(F.data.in_(["add_note", "view_notes", "delete_note"]), NoteStates.start)
async def process_main_menu(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "add_note":
        await state.set_state(NoteStates.add_note)
        await callback.message.answer("📝 Введите текст новой заметки:")
    elif callback.data == "view_notes":
        notes = await db.get_notes(callback.from_user.id)
        if notes:
            text = "\n\n".join(f"{i+1}. {note['note_text']}" for i, note in enumerate(notes))
            await callback.message.answer(
                f"📋 Ваши заметки:\n\n{text}",
                reply_markup=get_main_menu()  # <--- Добавляем клавиатуру после просмотра заметок
            )
        else:
            await callback.message.answer(
                "ℹ️ У вас пока нет заметок.",
                reply_markup=get_main_menu()  # <--- Добавляем клавиатуру, если заметок нет
            )
    elif callback.data == "delete_note":
        notes = await db.get_notes(callback.from_user.id)
        if notes:
            await state.set_state(NoteStates.delete_note)
            await callback.message.answer(
                "🗑️ Выберите заметку для удаления:",
                reply_markup=get_delete_menu(notes)
            )
        else:
            await callback.message.answer(
                "ℹ️ У вас пока нет заметок для удаления.",
                reply_markup=get_main_menu()  # <--- Добавляем клавиатуру, если заметок нет
            )
    await callback.answer()

@dp.message(NoteStates.add_note)
async def process_add_note(message: types.Message, state: FSMContext):
    await db.add_note(message.from_user.id, message.text)
    await message.answer("✅ Заметка успешно добавлена!", reply_markup=get_main_menu())
    await state.set_state(NoteStates.start)

@dp.callback_query(F.data.startswith("delete_"), NoteStates.delete_note)
async def process_delete_note(callback: types.CallbackQuery, state: FSMContext):
    note_id = int(callback.data.split("_")[1])
    notes = await db.get_notes(callback.from_user.id)  # Получаем список заметок
    note_to_delete = next((note for note in notes if note['id'] == note_id), None)  # Находим заметку по ID
    if note_to_delete and await db.delete_note(callback.from_user.id, note_id):
        await callback.message.answer(
            f"✅ Заметка \"{note_to_delete['note_text'][:30]}\" успешно удалена!",
            reply_markup=get_main_menu()
        )
    else:
        await callback.message.answer("❌ Ошибка при удалении заметки.", reply_markup=get_main_menu())
    await state.set_state(NoteStates.start)
    await callback.answer()

@dp.callback_query(F.data == "cancel")
async def process_cancel(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(NoteStates.start)
    await callback.message.answer("🔙 Действие отменено.", reply_markup=get_main_menu())
    await callback.answer()

async def on_startup():
    await db.create_pool()
    logger.info("Бот успешно запущен!")
    print("Bot ready")

async def on_shutdown():
    await db.pool.close()
    logger.info("Бот корректно завершил работу")

async def main():
    await on_startup()
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown()

if __name__ == '__main__':
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")