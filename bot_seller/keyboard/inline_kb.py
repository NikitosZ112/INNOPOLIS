from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn1 = InlineKeyboardButton(text='Суп', callback_data='soup')
btn2 = InlineKeyboardButton(text='Каша', callback_data='porridge')
btn3 = InlineKeyboardButton(text='Картошка', callback_data='potato')
btn4 = InlineKeyboardButton(text='Макароны', callback_data='pasta')

keyboard_inline = InlineKeyboardMarkup(inline_keyboard=[
    [btn1], [btn2], [btn3], [btn4]
])

kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сок', callback_data='juice')],
    [InlineKeyboardButton(text='Чай', callback_data='tea')],
    [InlineKeyboardButton(text='Компот', callback_data='compote')],
    [InlineKeyboardButton(text='Кола', callback_data='cola')],

])

payment_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Оплатить", pay=True)],
    [InlineKeyboardButton(text="Отмена", callback_data="cancel_payment")]
])