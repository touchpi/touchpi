import unittest

import touchpi.common
import touchpi.common.config
from touchpi.app.digitalclock import ClockApp
from touchpi.api.clockApi import ClockApi
from apscheduler.job import Job
from datetime import datetime


class TestClockApp(unittest.TestCase):

    def test_get_layout(self):
        self.assertIs(type(ClockApp.apps_layouts()), list)

    def test_clock_app(self):
        an_api = ClockApi()
        touchpi.common.start_scheduler()
        an_api.start()

        an_app = ClockApp(an_api)
        self.assertEqual(an_app.is_clock_running, True)

        a_job = an_app.weather_api.get_job(an_app.weather_api.job)
        self.assertIs(type(a_job), Job)
        self.assertIs(type(a_job.next_run_time), datetime)
        an_app.post_trigger()
        self.assertEqual(a_job.next_run_time, None)
        an_app.pre_trigger()
        self.assertIs(type(a_job.next_run_time), datetime)

        an_app.update("Clock", None)
        self.assertEqual(an_app.is_clock_running, False)
        an_app.update("Clock", None)
        self.assertEqual(an_app.is_clock_running, True)


if __name__ == '__main__':
    unittest.main()
