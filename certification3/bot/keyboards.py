from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_delete_task_keyboard(tasks):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Удалить {task['id']}", callback_data=f"delete_{task['id']}")]
        for task in tasks
    ])
    return keyboard