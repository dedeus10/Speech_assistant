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
def record_audio(ask=False):
    
    with sr.Microphone() as source: # microphone as source
        #r.adjust_for_ambient_noise(source)
        if ask:
            speak(ask)
        audio = r.listen(source)  # listen for the audio via source
        voice_data = ''
        try:
            print(ANA.name+': '+ANA.memory['Hello'])
            speak(ANA.name+': '+ANA.memory['Hello'])
            time.sleep(1)

            voice_data = r.recognize_google(audio)  # convert audio to text
            speak(voice_data)
        except sr.UnknownValueError: # error: recognizer does not understand
            speak('I did not get that')
        except sr.RequestError:
            speak('Sorry, the service is down') # error: recognizer is not connected
        print(f">> {voice_data.lower()}") # print what user said
        return voice_data.lower()

# get string and make a audio file to be played
def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en') # text to speech(voice)
    r = random.randint(1,20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file) # save as mp3
    playsound.playsound(audio_file) # play the audio file
    print(audio_string) # print what app said
    os.remove(audio_file) # remove audio file

if __name__ == "__main__":
    time.sleep(1)

    ANA = create_assistant('Ana')
    ANA.setMemory('Hello','Hello, How can I help you ?')
    print("Ana was born")
    while(1):
        voice_data = record_audio() # get the voice input

