import unittest
from touchpi.app.system import SystemApp


class TestSystemApp(unittest.TestCase):

    def test_get_layout(self):
        self.assertIs(type(SystemApp.apps_layouts()), list)


if __name__ == '__main__':
    unittest.main()
