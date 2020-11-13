#Import the libs which we need
import speech_recognition as sr # recognise speech


r = sr.Recognizer() # initialise a recogniser

with sr.Microphone() as source: # microphone as source
    
    r.adjust_for_ambient_noise(source)
    print("###### Say something ##########")
    audio = r.listen(source)
    with open('speech.wav','wb') as f:
        f.write(audio.get_wav_data())
    print(audio)
    try:
        print("###### A ##########")
        voice_data = r.recognize_google(audio, language='pt-BR')  # convert audio to text
        print(voice_data)
    except sr.UnknownValueError: # error: recognizer does not understand
        print('I did not get that')
    
