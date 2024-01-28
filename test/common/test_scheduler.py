import unittest
from apscheduler.schedulers.background import BackgroundScheduler
from touchpi.appbase.scheduler import scheduler, add_onetime_job_now, add_onetime_job, \
     modify_job, get_job, next_run_time_in_seconds
from touchpi.common.config import log
from touchpi.common import start_scheduler
from datetime import datetime, timedelta
from time import sleep
# import pytz


i = 0
start_scheduler()


class TestScheduler(unittest.TestCase):
    def test_onetime_job_now(self):
        global i

        def a_job():
            global i
            i = i + 1
            sleep(0.5)

        self.assertEqual(i, 0)  # a_job did not run
        self.assertTrue(type(scheduler) is BackgroundScheduler)
        job_id = add_onetime_job_now(a_job)
        self.assertTrue(type(job_id) is str)  # a successfully created job_id is a str
        self.assertTrue(len(job_id) > 0)  # a successfully created job_id is not empty
        self.assertEqual(i, 1)  # a_job started immediately and global variable i is changed at once
        self.assertTrue(get_job(job_id) is None)  # no job_id left because one time job has started

    def test_onetime_job(self):

        def a_job():
            pass

        job_id = add_onetime_job(a_job, next_run_time=datetime.now() + timedelta(seconds=1))
        sleep(0.4)
        self.assertTrue(get_job(job_id) is not None)  # job id valid because one time job has not started
        sleep(1)
        self.assertTrue(get_job(job_id) is None)  # no job id because one time job has started

    def test_modify_onetime_job(self):
        # tz = pytz.timezone('Europe/Berlin')  # use tz as parameter in datetime

        def a_job():
            log.debug("Scheduled job in test_modify_onetime_job done")

        job_id = add_onetime_job(a_job, next_run_time=next_run_time_in_seconds(1))
        log.info("Job scheduled in 1 second. " + str(get_job(job_id)))
        sleep(0.5)
        log.info("Waited 0.5s)")
        self.assertTrue(get_job(job_id) is not None)  # job id valid because one time job has not started

        modify_job(job_id, next_run_time=next_run_time_in_seconds(2))
        log.info("Job modified delayed 2 second.)" + str(get_job(job_id)))

        sleep(0.5)
        log.info("Waited 0,5 s)")
        self.assertTrue(get_job(job_id) is not None)  # job id valid because one time job has not started
        sleep(1)
        log.info("Waited 1,5 s)")
        self.assertTrue(get_job(job_id) is not None)  # job id valid because one time job has not started
        sleep(1)
        log.info("Waited 2,5 s)")
        self.assertTrue(get_job(job_id) is None)  # no job id because one time job has started


if __name__ == '__main__':
    unittest.main()
