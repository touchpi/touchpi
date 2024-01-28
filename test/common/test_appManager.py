import unittest
from touchpi.common.appManager import AppManager
from touchpi.common.api import Api

import touchpi.common
import touchpi.common.config


class TestAppManager(unittest.TestCase):
    def test_appManager(self):
        app_manager = AppManager(touchpi.common.start_scheduler())
        self.assertGreater(len(app_manager.apps), 0)
        self.assertEqual(app_manager.max_screen, len(app_manager.apps)-1)
        line = []
        app_manager.insert_app_layouts(line)
        self.assertEqual(len(line), len(app_manager.apps))


if __name__ == '__main__':
    unittest.main()
