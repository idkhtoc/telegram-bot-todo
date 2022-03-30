from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    new_task_state = State()
    time_state = State()