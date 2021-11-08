import sys
import requests
import datetime

#https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/[location]/[date1]/[date2]?key=YOUR_API_KEY 

class Weather_info:

    BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'

    def __init__(self, api_key, date=str(datetime.datetime.today().date() + datetime.timedelta(1))):
        self.api_key = api_key
        self.date = date
        self.location = 'Warsaw'
        self.info = self.get_info()
        
    def get_info(self):
        self.url_parameters = '&include=current&elements=precip,datetime,precipprob'
        request_url = f'{self.BASE_URL}/{self.location}/{self.date}?key={self.api_key}{self.url_parameters}'
        r = requests.get(request_url)
        info = r.json()
        return info

    def get_precip_info(self):
        precip = float(self.info['days'][0]['precip'])
        print(precip)
        return self.get_rain_chance(precip)

    def get_rain_chance(self, precip):
        if precip > 0.0:
            return 'Będzie padać.'
        elif precip == 0.0:
            return 'Nie będzie padać.'
        else:
            return 'Nie wiem.'

if len(sys.argv) == 2:
    weather = Weather_info(api_key=sys.argv[1])
elif len(sys.argv) == 3:
    weather = Weather_info(api_key=sys.argv[1], date=sys.argv[2])
else:
    print('Wprowadzono błędne dane.')
    quit()
    
print(weather.date)
print(weather.get_info())
print(weather.get_precip_info())



'''warsaw_lat = 52.25
warsaw_lon = 21'''