from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery
from aiogram.types.message import ContentType
from keyboard.inline_kb import payment_kb, keyboard_inline, kb
from states.state_bot import MenuState
from config import PROVIDER_TOKEN

router = Router()

@router.message(Command('start'))
async def start_bot(m: Message):
    await m.answer(
        "Привет! Я бот для заказа еды. Чтобы начать, нажмите /buy.",
        reply_markup=keyboard_inline  # Клавиатура с основными блюдами
    )

@router.message(Command('buy'))
async def buy_func(m: Message, state: FSMContext):
    await m.answer('Выберите основное блюдо:', reply_markup=keyboard_inline)
    await state.set_state(MenuState.main_course_state)

@router.callback_query(lambda cb: cb.data == "cancel_payment")
async def cancel_order(cb: CallbackQuery, state: FSMContext):
    await cb.answer("Заказ отменен.")
    await state.clear()  # Очищаем состояние FSM
    await cb.message.answer(
        "Заказ отменен. Вы можете начать заново.",
        reply_markup=keyboard_inline  # Возвращаемся к выбору основного блюда
    )

@router.callback_query(lambda cb: cb.data in ['soup', 'porridge', 'potato', 'pasta'])
async def callback(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    choice = {
        'soup': 'суп',
        'porridge': 'каша',
        'potato': 'картошку',
        'pasta': 'макароны'
    }.get(cb.data)
    price = {
        'soup': 100,
        'porridge': 80,
        'potato': 100,
        'pasta': 50
    }.get(cb.data)
    await state.update_data(main_course=cb.data, price=price)
    await cb.message.answer(f'Вы выбрали {choice} за {price} руб.')
    await cb.message.answer('Выберите напиток:', reply_markup=kb)
    await state.set_state(MenuState.drink_state)

@router.callback_query(lambda cb: cb.data in ['juice', 'tea', 'compote', 'cola'], StateFilter('MenuState:drink_state'))
async def get_drink(cb: CallbackQuery, state: FSMContext):
    drink_price = {
        'juice': 50,
        'tea': 30,
        'compote': 75,
        'cola': 150
    }.get(cb.data)
    data = await state.get_data()
    total = data['price'] + drink_price
    await state.update_data(drink=cb.data, total=total)
    await cb.message.answer_invoice(
        title="Оплата заказа",
        description=f"Оплата {data['main_course']} и {cb.data}",
        payload="payment",
        provider_token=PROVIDER_TOKEN,
        currency="RUB",
        prices=[
            {'label': f"{data['main_course']}", 'amount': data['price'] * 100},
            {'label': f"{cb.data}", 'amount': drink_price * 100}
        ],
        start_parameter="test-payment",
        reply_markup=payment_kb
    )

@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_payment(message: Message, state: FSMContext):
    data = await state.get_data()
    payment_info = message.successful_payment
    await message.answer("Оплата прошла успешно! Спасибо за заказ.")
    await state.clear()