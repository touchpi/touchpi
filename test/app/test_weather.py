import unittest

import touchpi.common
import touchpi.common.config
from touchpi.app.weather import WeatherApp
from touchpi.api.weatherApi import WeatherApi
from apscheduler.job import Job
from datetime import datetime


class TestWeatherApp(unittest.TestCase):

    def test_get_layout(self):
        self.assertIs(type(WeatherApp.apps_layouts()), list)

    def test_clock_app(self):
        an_api = WeatherApi()
        touchpi.common.start_scheduler()
        an_api.start()

        an_app = WeatherApp(an_api)

        a_job = an_app.weather_api.get_job(an_app.weather_api.job)
        self.assertIs(type(a_job), Job)
        self.assertIs(type(a_job.next_run_time), datetime)


if __name__ == '__main__':
    unittest.main()
