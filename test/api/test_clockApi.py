import unittest
from touchpi.api.clockApi import ClockApi
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


class TestClockApi(unittest.TestCase):
    scheduler = BackgroundScheduler(timezone="Europe/Berlin")
    clock_api = ClockApi(scheduler)

    def test_get_data(self):
        self.assertEqual(self.clock_api.get_data(), {'date': "",
                                                     'day': "",
                                                     'time': ""})

    def test_get_rawdata(self):
        self.assertIs(type(self.clock_api.get_rawdata()), datetime)


if __name__ == '__main__':
    unittest.main()
