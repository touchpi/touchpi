import unittest
from PySimpleGUI import Window
from touchpi.appbase.app import App


class TestApp(unittest.TestCase):
    def test_app(self):
        app = App(False)
        self.assertEqual(app.window, None)
        app = App(True)
        self.assertTrue(type(app.window) is Window)


if __name__ == '__main__':
    unittest.main()
