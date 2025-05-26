from aiogram.fsm.state import State, StatesGroup

class MenuState(StatesGroup):
    main_course_state = State()
    drink_state = State()