#Import the libs which we need
import speech_recognition as sr # recognise speech
import playsound # to play an audio file
from gtts import gTTS # google text to speech
import random
from time import ctime # get time details
import webbrowser # open browser
import ssl
import time
import os # to remove created audio files
from creating_service import *

r = sr.Recognizer() # initialise a recogniser
# listen for audio and convert it to text:
def record_audio():
    
    with sr.Microphone() as source: # microphone as source
        #r.adjust_for_ambient_noise(source)
        audio = r.listen(source)  # listen for the audio via source
        voice_data = ''
        try:
            print('---> ')
            voice_data = r.recognize_google(audio)  # convert audio to text
            ANA.speak(voice_data)
            
            ANA.search_service(voice_data.lower())
            
        except sr.UnknownValueError: # error: recognizer does not understand
            ANA.speak('I did not get that')
        except sr.RequestError:
            ANA.speak('Sorry, the service is down') # error: recognizer is not connected
        print(f">> {voice_data.lower()}") # print what user said
        return voice_data.lower()


if __name__ == "__main__":
    time.sleep(1)
    #Create weather service
    w = weather_interface('Santa Maria', 'BR')

    #Create ANA assistant
    # A: Artificial
    # N: Natural
    # A: Assistant
    ANA = create_assistant('Ana',w)
    ANA.setMemory('Hello','Hello, How can I help you ?')
    ANA.create_brain()
    print("Ana was born!")
    
    ANA.speak(ANA.name+': '+ANA.memory['Hello'])
    time.sleep(1)
    while(1):
        voice_data = record_audio() # get the voice input

