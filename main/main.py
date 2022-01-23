from loader import db
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from loader import bot
from states.states import Text_or_word
from keyboards import keyborads
from data_fetcher import data_fetcher
from googletrans import Translator

translator = Translator()
@db.message_handler(Command('language'), state='*')
async def language_change(msg:Message,state:FSMContext):
    await bot.send_message(msg.chat.id, '🇺🇿Tillni tanlang \n🇷🇺Выберите предпочитаемый язык \n🇬🇧Choose your language',
                           reply_markup=keyborads.language)
    await Text_or_word.language.set()
@db.message_handler(Command('start'), state='*')
async def start(msg:Message):
    await bot.send_message(msg.chat.id,'🇺🇿Tillni tanlang \n🇷🇺Выберите предпочитаемый язык \n🇬🇧Choose your language', reply_markup=keyborads.language)
    await Text_or_word.language.set()
@db.message_handler(state=Text_or_word.language)
async def start(msg:Message, state:FSMContext):
    text = msg.text
    if text == 'Uzbek':
        mark_up = await keyborads.method('uz')
        await state.update_data({
            'language':'uz'
        })
        await bot.send_message(msg.chat.id,'📚Tarjima uchun tarjimani bosing'
                                           '\n🔎Teksni tekshirish uchun Tekshirish bosing' ,reply_markup=mark_up)
    elif text == 'English':
        mark_up =await keyborads.method('en')
        await state.update_data({
            'language': 'en'
        })
        await bot.send_message(msg.chat.id, '📚Press a Translate for translate'
                                            '\n🔎Press a Check for checking mistakes in text', reply_markup=mark_up)
    elif text == 'Русский':
        mark_up = await keyborads.method('ru')
        await state.update_data({
            'language': 'ru'
        })
        await bot.send_message(msg.chat.id, '📚Для перевода нажмите перевод. '
                                            '\n🔎Для проверки текста нажмите проверка', reply_markup=mark_up)
    await Text_or_word.text_or_word.set()
@db.message_handler(state=Text_or_word.text_or_word)
async def text_or_word_def(msg:Message, state: FSMContext):
    sta = await state.get_state()
    lang = await state.get_data()
    lang = lang['language']
    text = msg.text
    if text == 'перевод' or text == 'Translate' or text == 'Tarjima':
        await Text_or_word.word.set()
        if lang == 'ru':
            # await bot.send_message(msg.chat.id,'Если вы отправите слово, вы получите все значения и аудио слов. '
            #                        '\nЕсли вы отправите предложение, вы получите только перевод')
            await bot.send_message(msg.chat.id,'✏️Отправьте слова Для значение \nили предложение Для перевода', reply_markup=ReplyKeyboardRemove())
        elif lang == 'uz':
            # await bot.send_message(msg.chat.id, 'Bitta so`z tashlasangiz o`sha so`zning barcha manosini va audiosini olasiz'
            #                                     '\nAgar gap tashlasabgiz faqat gina tarjimasini olasiz')
            await bot.send_message(msg.chat.id, '✏️bita so`z tashlasangiz manisini olasiz\nGap tashlasangiz tarjima olasiz', reply_markup=ReplyKeyboardRemove())
        elif lang == 'en':
            # await bot.send_message(msg.chat.id, 'If you send a word, you will get all the meanings and audio of the word'
            #                                     '\nIf you send a sentence, you will only get a translation')
            await bot.send_message(msg.chat.id, '✏️Send word for meanings \nor sentence for translations', reply_markup=ReplyKeyboardRemove())
    elif text == 'Tekshirish' or text == 'Check' or text == 'проверка':
        if lang == 'ru':
            await bot.send_message(msg.chat.id,'📝Отправьте Английский текст ', reply_markup=ReplyKeyboardRemove())
        elif lang == 'uz':
            await bot.send_message(msg.chat.id, '📝Inglizcha Tekstni tashlang', reply_markup=ReplyKeyboardRemove())
        elif lang == 'en':
            await bot.send_message(msg.chat.id, '📝Send me your textin English',reply_markup=ReplyKeyboardRemove())
        await Text_or_word.text.set()
    elif text =='View' or text == 'Посмотреть' or text=='ko`rish':
        data = await state.get_data()
        amount = data['amount_mistake']
        for i in range(0,amount):
            mistakes = data[f'mistake{i}']
            if lang == 'en':
                mark_up = await keyborads.method('en')
                if i == (amount -1):
                    await bot.send_message(msg.chat.id,f' ❎ERROR {i+1}: {mistakes[0]}'
                                                       f'\n⛳️In sentance: {mistakes[1]}'
                                                       f'\n👉description: {mistakes[2]}', reply_markup=mark_up)
                else:
                    await bot.send_message(msg.chat.id, f' ❎ERROR {i+1}: {mistakes[0]}'
                                                        f'\n⛳️In sentance: {mistakes[1]}'
                                                        f'\n👉description: {mistakes[2]}')
            if lang == 'uz':

                mark_up = await keyborads.method('uz')
                error_tran = translator.translate(text= mistakes[0], dest=lang).text
                des_trans = translator.translate(text=mistakes[2], dest=lang).text
                if i == (amount -1):
                    await bot.send_message(msg.chat.id,f' ❎{i+1}-Xatolik:🇺🇿{error_tran} \n🇬🇧{mistakes[0]}'
                                                       f'\n\n⛳️Shu qatorda: {mistakes[1]}'
                                                       f'\n\n👉Tafsif:🇺🇿{des_trans} \n🇬🇧{mistakes[2]}', reply_markup=mark_up)
                else:
                    await bot.send_message(msg.chat.id, f' ❎{i + 1}-Xatolik: 🇺🇿{error_tran} \n🇬🇧{mistakes[0]}'
                                                        f'\n\n⛳️Shu qatorda: {mistakes[1]}'
                                                        f'\n\n👉Tafsif: 🇺🇿{des_trans} \n🇬🇧{mistakes[2]}')
            if lang == 'ru':
                mark_up =await keyborads.method('ru')
                error_tran = translator.translate(text=mistakes[0], dest=lang).text
                des_trans = translator.translate(text=mistakes[2], dest=lang).text
                if i == (amount -1):
                    await bot.send_message(msg.chat.id,f' ❎{i+1}-Ошибка:🇷🇺{error_tran} \n🇬🇧{mistakes[0]}'
                                                       f'\n\n⛳️В тексте: {mistakes[1]}'
                                                       f'\n\n👉описание:{des_trans} \n🇬🇧{mistakes[2]}', reply_markup=mark_up)
                else:
                    await bot.send_message(msg.chat.id, f' ❎{i + 1}-Ошибка:🇷🇺{error_tran} \n🇬🇧{mistakes[0]}'
                                                        f'\n\n⛳️В тексте: {mistakes[1]}'
                                                        f'\n\n👉описание:{des_trans} \n🇬🇧{mistakes[2]}')
    elif text == 'Definitions' or text == 'Manolari' or text == 'значение':
        data = await state.get_data()
        mark_up = await keyborads.method(lang)
        defs_amount = data['definitions_number']
        for i in range(0,defs_amount):
            defs = data[f'definitions{i+1}']
            if lang =='en':
                await bot.send_message(msg.chat.id,f'🎯Definition {i+1}: {defs}', reply_markup=mark_up)
            if lang =='uz':
                await bot.send_message(msg.chat.id,f'🎯{i+1}-Manosi:🇺🇿{translator.translate(text=defs,dest=lang).text} \n🇬🇧{defs}', reply_markup=mark_up)
            if lang =='ru':
                await bot.send_message(msg.chat.id,f'🎯значение {i+1}:🇷🇺{translator.translate(text=defs,dest=lang).text} \n🇬🇧{defs}', reply_markup=mark_up)
    else:
        if lang =='uz':
            await bot.send_message(msg.chat.id,'🤦Tugmani bosing')
        if lang =='en':
            await bot.send_message(msg.chat.id,'🤦Press one of the keyboards')
@db.message_handler(state=Text_or_word.text)
async def text_detetxtor(msg:Message,state:FSMContext):
    text = msg.text
    data = await data_fetcher.text_checker(text)
    lang = await state.get_data()
    lang = lang['language']
    mark_up = await  keyborads.method(lang)
    if data == False:
        if lang == 'en':
            await bot.send_message(msg.chat.id,'🎉🥳We could not find a mistake', reply_markup=mark_up)
        if lang =='ru':
            mark_up = await keyborads.method('ru')
            await bot.send_message(msg.chat.id , '🎉🥳Ошибки не найдено',reply_markup=mark_up)
        if lang =='uz':
            mark_up =await keyborads.method('uz')
            await bot.send_message(msg.chat.id , '🎉🥳xatolik topilmadi',reply_markup=mark_up)
        await Text_or_word.text_or_word.set()
    else:
        mistake = 0
        mark =await keyborads.method('en')
        for i in range(0,len(data)):
            await state.update_data({
                f'mistake{i}':[data[i]["message"],data[i]["sentence"],data[i]["description"]]})
            mistake += 1
        await state.update_data({'amount_mistake': mistake})
        if lang=='en':
            add = await keyborads.review_keyboard('View')
            all = mark.add(add)
            await bot.send_message(msg.chat.id,f'🤦{mistake} mistakes were found', reply_markup=all)
        if lang =='ru':
            add = await keyborads.review_keyboard('Посмотреть')
            all = mark.add(add)
            await bot.send_message(msg.chat.id, f'🤦{mistake} Ошибки найдено', reply_markup=all)
        if lang=='uz':
            add = await keyborads.review_keyboard('ko`rish')
            all = mark.add(add)
            await bot.send_message(msg.chat.id,f'🤦{mistake} ta xatolik topildi', reply_markup=all)
        await Text_or_word.text_or_word.set()
@db.message_handler(state=Text_or_word.word)
async def text_translator(msg:Message,state:FSMContext):
    text = msg.text
    text_lang = translator.detect(text=text).lang
    data = await state.get_data()
    lang = data['language']
    mark_up =await keyborads.method(lang)

    if len(text.split()) > 2:
        if lang != text_lang:
            translated_text = translator.translate(text=text, dest=lang).text
            await data_fetcher.audio_data(translated_text)
            audio = open('welcome.mp3', 'rb')
            await bot.send_audio(msg.chat.id, audio)
            audio.close()
            await msg.reply(f'♻️ {translated_text}', reply_markup=mark_up)

        else:
            translated_text = translator.translate(text=text, dest='en').text
            await data_fetcher.audio_data(translated_text)
            audio = open('welcome.mp3', 'rb')
            await bot.send_audio(msg.chat.id, audio)
            audio.close()
            await msg.reply(f'♻️ {translated_text}', reply_markup=mark_up)

    else:

        add_key = await keyborads.dfinations_keyboard(lang)
        translated_text = translator.translate(text=text, dest='en').text
        definat = await data_fetcher.word_definations(text=translated_text)
        if definat == False:
            if lang=='en':
                await msg.reply('🤷we could find any definitions')
            else:
                d = await data_fetcher.audio_data(translated_text)
                audio = open('welcome.mp3', 'rb')
                await bot.send_audio(msg.chat.id, audio)
                audio.close()
                await bot.send_message(msg.chat.id, f'♻️ {translated_text}', reply_markup=mark_up)

        else:
            mark_up1 = mark_up.add(add_key)
            d = await data_fetcher.audio_data(translated_text)
            audio = open('welcome.mp3', 'rb')
            await bot.send_audio(msg.chat.id, audio)
            audio.close()
            await bot.send_message(msg.chat.id, f'♻️ {translated_text}', reply_markup=mark_up1)

            count = 1
            for dat in definat:
                await state.update_data({
                    f'definitions{count}': f'{dat}',
                    'definitions_number' : count
                })
                count +=1
    await Text_or_word.text_or_word.set()
