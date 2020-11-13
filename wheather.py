from pyowm import OWM 
class Openwinterface():
    def __init__(self, cidade,pais):
 
        #retorna um dicionário com os dados do openweather
        self.cidade = cidade
        self.pais = pais
 
    def get_weather(self):
 
        owm = OWM('Key')  # You MUST provide a valid API key
        posicao = "%s,%s" % (self.cidade,self.pais)        # definimos o local aonde serão obtidos os dados
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(posicao)
         
        w = observation.weather
        print(w)                  # <Weather - reference time=2013-12-18 09:20, status=Clouds>

        # Weather details
        wind = w.wind()
        hum = w.humidity
        temp = w.temperature('celsius')
        print("Wind: ",wind['speed'])                  # {'speed': 4.6, 'deg': 330}
        print("Humidity: ", hum)                # 87
        print("Temp: ",temp['temp'])  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

print("Initializing...")
w = Openwinterface('Santa Maria', 'BR')
w.get_weather()
