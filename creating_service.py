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


class weather_interface():
    def __init__(self, cidade,pais):
 
        #retorna um dicionário com os dados do openweather
        self.weather={}
        self.cidade = cidade
        self.pais = pais
 
    def get_weather(self):
 
        owm = OWM('73b7cb8a41b103d02adb89fc55125da9')  # You MUST provide a valid API key
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

