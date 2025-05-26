from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn1 = KeyboardButton(text='Кнопка 1')
btn2 = KeyboardButton(text='Кнопка 2')

keyboard_reply = ReplyKeyboardMarkup(keyboard=[
    [btn1, btn2]
], resize_keyboard=True, one_time_keyboard=True)