#Import the libs which we need
import webbrowser # open browser
import ssl
import os # to remove created audio files
import playsound # to play an audio file
from gtts import gTTS # google text to speech
import random
from time import ctime # get time details
import time
from pyowm import OWM 
from nltk.corpus import stopwords
from gensim.models import Word2Vec
import bs4 as bs
import urllib.request
import re
import nltk


class create_assistant:
    def __init__(self, name, w):
        self.name = name
        self.memory = {'Name':self.name}
        self.weather_API = w
    def setMemory(self, key, txt):
        self.memory[key] = txt

    # get string and make a audio file to be played
    def speak(self,audio_string):
        tts = gTTS(text=audio_string, lang='en') # text to speech(voice)
        r = random.randint(1,20000000)
        audio_file = 'audio' + str(r) + '.mp3'
        tts.save(audio_file) # save as mp3
        playsound.playsound(audio_file) # play the audio file
        print(audio_string) # print what app said
        os.remove(audio_file) # remove audio file


    def search_service(self,voice_data):
         #search google
        if(("search for" in voice_data) and ('youtube' not in voice_data)):
            search_term = voice_data.split("for")[-1]
            url = f"https://google.com/search?q={search_term}"
            webbrowser.get().open(url)
            self.speak(f'Here is what I found for {search_term} on google')

         # search youtube
        if("youtube" in voice_data):
            search_term = voice_data.split("for")[-1]
            url = f"https://www.youtube.com/results?search_query={search_term}"
            webbrowser.get().open(url)
            self.speak(f'Here is what I found for {search_term} on youtube')

        if("time" in voice_data):
            from datetime import datetime

            date = datetime.now()
            date = date.strftime('%d/%m/%Y')
            self.speak(date)

            time.sleep(1)
            date = datetime.now()
            time_h = date.strftime('%H:%M')
            self.speak(time_h)

        if("weather" in voice_data):
            w_now = {}
            w_now = self.weather_API.get_weather()
            wind = w_now['wind']
            hum = w_now['humidity']
            temp = w_now['temp']

            self.speak('Todays weather is')
            
            self.speak(f'Wind of {wind} km/h')
            self.speak(f'Humidity of {hum} %')
            self.speak(f'Temperature of {temp} celsius')
        
        if("think" in voice_data):
            search_term = voice_data.split("of")[-1]
            suggestion = self.make_suggestion(search_term)
            txt = 'I believe that the word you are looking for is ' + str(suggestion[0])
            self.speak(txt)
            sug = int(suggestion[1]*100)
            txt = 'I am ' + str(sug) +' % sure that'
            self.speak(txt)

    def create_brain(self):
        scrapped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Artificial_intelligence')
        article = scrapped_data .read()

        parsed_article = bs.BeautifulSoup(article,'lxml')
        paragraphs = parsed_article.find_all('p')

        article_text = ""

        for p in paragraphs:
            article_text += p.text

        # Cleaing the text
        processed_article = article_text.lower()
        processed_article = re.sub('[^a-zA-Z]', ' ', processed_article )
        processed_article = re.sub(r'\s+', ' ', processed_article)

        # Preparing the dataset
        all_sentences = nltk.sent_tokenize(processed_article)

        all_words = [nltk.word_tokenize(sent) for sent in all_sentences]

        # Removing Stop Words
        from nltk.corpus import stopwords
        for i in range(len(all_words)):
            all_words[i] = [w for w in all_words[i] if w not in stopwords.words('english')]

        self.brain = Word2Vec(all_words, min_count=2)


    def make_suggestion(self, word):
        try:
            print("ANA is thinking about ", word)
            vocabulary = self.brain.wv.vocab
            print(vocabulary.keys())
            suggestions = self.brain.wv.most_similar('machine')
            print(suggestions[0])
            return suggestions[0]
        except:
            suggestions = ['None',0]
            return suggestions

class weather_interface():
    def __init__(self, cidade,pais):
 
        #retorna um dicionário com os dados do openweather
        self.weather={}
        self.cidade = cidade
        self.pais = pais
 
    def get_weather(self):
 
        owm = OWM('Your-Key')  # You MUST provide a valid API key
        posicao = "%s,%s" % (self.cidade,self.pais)        # definimos o local aonde serão obtidos os dados
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(posicao)
         
        w = observation.weather

        # Weather details
        wind = w.wind()
        hum = w.humidity
        temp = w.temperature('celsius')
        
        self.weather = {'wind':wind['speed'], 'humidity':hum, 'temp': temp['temp']}
        return self.weather

