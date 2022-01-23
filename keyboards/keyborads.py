from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
#tillni tanlash tugmalari
language = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
uzb = KeyboardButton(text='Uzbek')
eng = KeyboardButton(text = 'English')
ru = KeyboardButton(text = 'Русский')
language.add(uzb,eng,ru)

#amalni tanlash tugmasi teks / so`z
async def method(lan):
    if lan== 'uz':
        mark_up = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        tekt = KeyboardButton(text='Tarjima')
        wort = KeyboardButton(text='Tekshirish')
        mark_up.add(tekt, wort)
        return mark_up
    if lan== 'en':
        mark_up = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        tekt = KeyboardButton(text='Translate')
        wort = KeyboardButton(text='Check')
        mark_up.add(tekt, wort)
        return mark_up
    if lan== 'ru':
        mark_up = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        tekt = KeyboardButton(text='перевод')
        wort = KeyboardButton(text='проверка')
        mark_up.add(tekt, wort)
        return mark_up

#review keyboard
async def review_keyboard(text):
    review = KeyboardButton(text =text)
    return review
async def dfinations_keyboard(lang):
    if lang == 'en':
        mark_up = KeyboardButton(text=f'Definitions')
    elif lang == 'uz':
        mark_up = KeyboardButton(text='Manolari')
    elif lang == 'ru':
        mark_up = KeyboardButton(text='значение')
    return mark_up