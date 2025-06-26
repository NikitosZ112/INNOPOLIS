from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, InlineKeyboardButton

def get_delete_task_keyboard(tasks: list) -> InlineKeyboardBuilder:
    """Клавиатура для удаления задач"""
    builder = InlineKeyboardBuilder()
    for task in tasks:
        builder.button(
            text=f"❌ {task['name']}",
            callback_data=f"delete_{task['id']}"
        )
    builder.adjust(1)
    return builder.as_markup()

def get_cancel_keyboard() -> ReplyKeyboardBuilder:
    """Клавиатура для отмены действий"""
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Назад"))
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )