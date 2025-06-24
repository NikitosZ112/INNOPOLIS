from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_delete_task_keyboard(tasks: list):
    builder = InlineKeyboardBuilder()
    for task in tasks:
        builder.button(
            text=f"❌ {task['name']}",
            callback_data=f"delete_{task['id']}"
        )
    builder.adjust(1)
    return builder.as_markup()