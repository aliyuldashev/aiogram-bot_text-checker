from aiogram.dispatcher.filters.state import State,StatesGroup
class Text_or_word(StatesGroup):
    language = State()
    text_or_word = State()
    text = State()
    word = State()
    view = State()