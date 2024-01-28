import unittest
from touchpi.app_old.cloth import ClothApp


class TestClothApp(unittest.TestCase):

    def test_get_layout(self):
        self.assertIs(type(ClothApp.apps_layouts()), list)


if __name__ == '__main__':
    unittest.main()
