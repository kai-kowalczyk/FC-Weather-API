import sys
import requests
import datetime
import json
from pathlib import Path

# https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/[location]/[date1]/[date2]?key=YOUR_API_KEY


class Weather_info:

    BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'

    def __init__(self, api_key, date=str(datetime.datetime.today().date() + datetime.timedelta(1))):
        self.api_key = api_key
        self.date = date
        self.location = 'Warsaw'
        self.logs = 'weather_logs.json'
        self.precip = None
        self.rain_chance = None
        self.info = self.get_info()

    def get_info(self):
        if self.check_data_in_file() == False:
            self.url_parameters = '&include=current&elements=precip,datetime,precipprob&unitGroup=metric'
            request_url = f'{self.BASE_URL}/{self.location}/{self.date}?key={self.api_key}{self.url_parameters}'
            r = requests.get(request_url)
            info = r.json()
        else:
            quit()
        return info

    def get_precip_info(self):
        self.precip = float(self.info['days'][0]['precip'])
        return self.get_rain_chance(self.precip)

    def get_rain_chance(self, precip):
        if precip == 0.0:
            self.rain_chance = 'Nie będzie padać.'
        elif precip > 0.0:
            self.rain_chance = 'Będzie padać.'
        else:
            self.rain_chance = 'Nie wiem.'
        print(self.rain_chance)

    def check_if_file_exists(self):
        file_ex = Path(self.logs).exists()
        return file_ex

    def check_data_in_file(self):
        if self.check_if_file_exists() == True:
            with open(self.logs) as weather_data:
                data = json.load(weather_data)
                if self.date in data:
                    print(data.get(self.date))
                    return True
                else:
                    return False
        else:
            return False

    def save_data_to_file(self):
        with open(self.logs) as weather_data:
            data = json.load(weather_data)
        
        new_data = {self.date: self.rain_chance}
        data.update(new_data)

        with open(self.logs, 'w') as weather_data:
            json.dump(data, weather_data)


if len(sys.argv) == 2:
    weather = Weather_info(api_key=sys.argv[1])
    weather.get_precip_info()
    weather.save_data_to_file()
elif len(sys.argv) == 3:
    weather = Weather_info(api_key=sys.argv[1], date=sys.argv[2])
    weather.get_precip_info()
    weather.save_data_to_file()
else:
    print('Wprowadzono błędne dane.')
    quit()