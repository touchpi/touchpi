import unittest
from touchpi.api.weatherApi import WeatherApi, ForecastReturnValue
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


class TestWeatherApi(unittest.TestCase):
    scheduler = BackgroundScheduler(timezone="Europe/Berlin")
    weather_api = WeatherApi(scheduler)

    def test_get_data(self):
        self.assertEqual(self.weather_api.get_data(), {'actual_temp': "0 °C°",
                                                       'actual_icon': "50n.png",
                                                       "forecast_time": "Today",
                                                       'forecast_temp': "0 °C°",
                                                       'forecast_icon': "50n.png",
                                                       'forecast_text': "Unknown"})

    def test_actual_request(self):
        self.assertEqual(self.weather_api.actual_request, "https://api.openweathermap.org/data/2.5/weather"
                                                          "?lat=48.148926488749716&lon=11.477638834434837&units=metric"
                                                          "&appid=2415cd18a96d604ae5207854fa769f6d")
        print(self.weather_api.forecast_request)
        self.assertEqual(self.weather_api.forecast_request, "https://api.openweathermap.org/data/2.5/forecast?"
                                                            "lat=48.148926488749716&lon=11.477638834434837&"
                                                            "units=metric&appid=2415cd18a96d604ae5207854fa769f6d&"
                                                            "cnt=18")
        print(self.weather_api.forecast_request)

    def test_actual_data(self):
        actual_dict = self.weather_api.get_rawdata(self.weather_api.actual_request)
        self.assertIn("dt", actual_dict)
        self.assertIs(type(actual_dict['dt']), int)
        self.assertIn("main", actual_dict)
        self.assertIs(type(actual_dict['main']), dict)
        self.assertIn("weather", actual_dict)

        response_weather_list = actual_dict['weather']
        self.assertIs(type(response_weather_list), list)
        self.assertEqual(len(response_weather_list), 1)

        response_main_dict = actual_dict['main']
        self.assertIn("feels_like", response_main_dict)
        self.assertIs(type(response_main_dict['feels_like']), float)

        response_weather_dict = response_weather_list[0]
        self.assertIn("icon", response_weather_dict)
        self.assertIs(type(response_weather_dict['icon']), str)

    def test_forecast_data(self):
        forecast_dict = self.weather_api.get_rawdata(self.weather_api.forecast_request)
        self.assertIn("cod", forecast_dict)
        self.assertEqual(forecast_dict['cod'], "200")
        self.assertIn("cnt", forecast_dict)
        self.assertEqual(forecast_dict['cnt'], 18)
        self.assertIn("list", forecast_dict)
        self.assertIs(type(forecast_dict['list']), list)

        forecast_list = forecast_dict['list']
        self.assertIs(type(forecast_list), list)
        self.assertEqual(len(forecast_list), 18)

        def test_forecast_list(i):
            first_forecast_list = forecast_list[i]
            self.assertIs(type(first_forecast_list), dict)
            dt = datetime.utcfromtimestamp(first_forecast_list['dt'])
            self.assertIs(type(dt), datetime)
            main = first_forecast_list['main']
            self.assertIs(type(main), dict)
            self.assertIs(type(main['feels_like']), float)
            weather = first_forecast_list['weather']
            self.assertIs(type(weather), list)
            self.assertEqual(len(weather), 1)
            first_weather_list = weather[0]
            self.assertIs(type(first_weather_list['icon']), str)
            self.assertIs(type(first_weather_list['description']), str)

        test_forecast_list(0)
        test_forecast_list(17)

    def test_forecast_navigation(self):
        weather_api = WeatherApi(self.scheduler)
        weather_api.run_job()
        self.assertEqual(weather_api.forecast_index, 0)
        self.assertEqual(weather_api.set_forecast_minus(), ForecastReturnValue.START)
        self.assertEqual(weather_api.forecast_index, 0)
        self.assertEqual(weather_api.set_forecast_plus(), ForecastReturnValue.BETWEEN)
        self.assertEqual(weather_api.forecast_index, 1)
        self.assertEqual(weather_api.set_forecast_minus(), ForecastReturnValue.START)
        self.assertEqual(weather_api.forecast_index, 0)
        for i in range(7):
            self.assertEqual(weather_api.forecast_index, i)
            self.assertEqual(weather_api.set_forecast_plus(), ForecastReturnValue.BETWEEN)
        self.assertEqual(weather_api.set_forecast_plus(), ForecastReturnValue.END)


if __name__ == '__main__':
    unittest.main()
