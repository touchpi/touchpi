import unittest
from touchpi.common.date_helper import readable_date
from datetime import timedelta, datetime


class TestDateHelper(unittest.TestCase):
    def test_readable_date(self):
        now = datetime.now()
        time_now = now.strftime(" %H:%M")
        self.assertEqual(readable_date(now), "Today" + time_now)
        test_date = now + timedelta(days=1)
        self.assertEqual(readable_date(test_date), "Tomorrow" + time_now)
        test_date = now + timedelta(days=-1)
        self.assertEqual(readable_date(test_date), "Yesterday" + time_now)
        test_date = now + timedelta(days=2)
        formatted_testate = test_date.strftime("%d.%m %H:%M")
        self.assertEqual(readable_date(test_date), formatted_testate)
        test_date = now + timedelta(days=-2)
        formatted_testate = test_date.strftime("%d.%m %H:%M")
        self.assertEqual(readable_date(test_date), formatted_testate)


if __name__ == '__main__':
    unittest.main()
