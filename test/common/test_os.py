import unittest
from PySimpleGUI import Window
from touchpi.common.appManager import AppManager
from apscheduler.schedulers.background import BackgroundScheduler
from touchpi.common.os import OS


class TestOS(unittest.TestCase):
    def test_os(self):
        os = OS()
        self.assertEqual(os.screen, 0)
        self.assertTrue(type(os.window) is Window)
        self.assertTrue(type(os.appManager) is AppManager)
        self.assertTrue(type(os.scheduler) is BackgroundScheduler)
        # gui tests needed for make_invisible(), make_visible() and run()


if __name__ == '__main__':
    unittest.main()
