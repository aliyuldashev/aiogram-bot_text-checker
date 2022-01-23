from gtts import gTTS
import requests
async def text_checker(text):
    data = {
    'text': text,
    'language': 'en'
    }
    response = requests.post('https://api.languagetool.org/v2/check', data=data)
    data = response.json()
    errors = []
    try:
        for i in range(0,(len(data['matches']))):
            if data['matches'][i]['message'] == 'Possible typo: you repeated a whitespace':
                continue
            if data['matches'][i]['message'] == 'Possible spelling mistake found.':
                continue
            errors.append({'message':data['matches'][i]['message'] ,
                           'sentence':data['matches'][i]['context']['text'] ,
                           'description': data['matches'][i]['rule']['description']})
    except:
        return False
    if errors == []:
        return False
    return errors
async def word_definations(text):
    req = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{text}')
    data = req.json()

    definitions = []
    try:
        count = 0
        for dat in data[0]['meanings']:
            if count == 1:
                continue
            for da in dat['definitions']:
                definitions.append(da['definition'])
            count += 1
        return definitions
    except Exception as ex:
        print(ex, 10)
        return False

async def audio_data(text):
    mytext = text
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("welcome.mp3")