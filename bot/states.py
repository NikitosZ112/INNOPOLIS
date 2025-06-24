from aiogram.fsm.state import State, StatesGroup

class AddTaskStates(StatesGroup):
    name = State()
    deadline = State()