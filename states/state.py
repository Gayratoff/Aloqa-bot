from aiogram.dispatcher.filters.state import State, StatesGroup

class Add_user(StatesGroup):
    full_name = State()
    number = State()
    city = State()

class Aloqa(StatesGroup):
    aloqa = State()