from touchpi.appbase.app import App, log, settings
from touchpi.appbase.scheduler import add_interval_job_now, remove_job
from requests import get
from datetime import datetime, date


class OpenWeather(App):
    def __init__(self):
        super().__init__()
        self.job = None
        self.actual_temp = "0 °C°"
        self.actual_icon = "50n.png"
        self.forecast_list = []
        request_parameter = "lat=" + settings.openweather_latitude
        request_parameter += "&lon=" + settings.openweather_longitude
        request_parameter += "&units=" + settings.openweather_units
        request_parameter += "&appid=" + settings.openweather_appid
        self.actual_request = settings.openweather_actual + request_parameter
        self.forecast_request = settings.openweather_forecast + request_parameter + "&cnt=18"
        self.do_long_operation()
        log.info("OpenWeather initialised.")

    @staticmethod
    def readable_date(dt):
        diff = (dt.date() - date.today()).days
        t = dt.strftime("%H:%M")
        if diff == 0:
            d = "Today"
        elif diff == -1:
            d = "Yesterday"
        elif diff == 1:
            d = "Tomorrow"
        else:
            d = dt.strftime("%d.%m")
        return d + " " + t

    def do_long_operation(self):
        self.job = add_interval_job_now(self.run_job, minutes=settings.openweather_job_intervall_min)
        log.info("WeatherApi Job started.")

    def close_trigger(self):
        remove_job(self.job)

    def run_job(self):
        try:
            actual_data = self.get_rawdata(self.actual_request)
            forecast_data = self.get_rawdata(self.forecast_request)
            self.convert_rawdata(actual_data, forecast_data)
            log.info(self.get_data())
            self.write_safe_event_value("openweather_data", self.get_data())
        except Exception as err:
            log.error("Error in loading data: " + str(err) + " " + str(type(err)))

    @staticmethod
    def get_rawdata(request):
        r = get(request)
        log.debug("URL Response: " + str(r) + " of request: " + str(request))
        return r

    def convert_rawdata(self, actual_data, forecast_data):
        actual_data = actual_data.json()
        actual_list = actual_data['weather']
        actual_main_dict = actual_data['main']
        actual_weather_dict = actual_list[0]
        self.actual_temp = str(round(actual_main_dict['feels_like'], 1)) + " °C"
        self.actual_icon = actual_weather_dict['icon'] + ".png"

        forecast_data = forecast_data.json()
        forecast_list = forecast_data['list'][1::2]
        reduced_forecast_list = []
        for fl in forecast_list:
            reduced_forecast_list.append({'time': OpenWeather.readable_date(datetime.utcfromtimestamp(fl['dt'])),
                                          'temp': str(round(fl['main']['feels_like'], 1)) + " °C",
                                          'icon': fl['weather'][0]['icon'] + '.png',
                                          'text': fl['weather'][0]['description'],
                                          })
        self.forecast_list = reduced_forecast_list

    def get_data(self):
        d = {"actual_temp": self.actual_temp,
             "actual_icon": self.actual_icon,
             "forecast_list": self.forecast_list}
        return d


if __name__ == '__main__':
    app = OpenWeather()
    app.run()
