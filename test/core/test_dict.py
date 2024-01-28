import unittest
from sys import version_info


class TestDict(unittest.TestCase):

    def test_python_version(self):
        self.assertGreaterEqual(version_info, (3, 6))

    def test_update_dict(self):
        foreground_apps = {'1': None, '2': None, '3': None}
        self.assertDictEqual(foreground_apps, {'1': None, '2': None, '3': None})
        foreground_apps["2"] = "app2"
        self.assertDictEqual(foreground_apps, {'1': None, '2': "app2", '3': None})
        foreground_apps.update({"2": None})
        self.assertDictEqual(foreground_apps, {'1': None, '2': None, '3': None})
        if "4" in foreground_apps:
            foreground_apps["4"] = "app4"
        self.assertDictEqual(foreground_apps, {'1': None, '2': None, '3': None})

    def test_del_dict(self):
        foreground_apps = {'1': None, '2': None, '3': None, '4': None, '5': None, '6': None, '7': None}
        del foreground_apps["4"]
        self.assertEqual(foreground_apps, {'1': None, '2': None, '3': None, '5': None, '6': None, '7': None})
        if "x" in foreground_apps:
            del foreground_apps["x"]
        self.assertEqual(foreground_apps, {'1': None, '2': None, '3': None, '5': None, '6': None, '7': None})

    def test_dict_list_order(self):
        apps = ["1", "2", "3", "4", "5", "6", "7"]
        foreground_apps = {str(key): None for key in apps}
        self.assertEqual(foreground_apps, {'1': None, '2': None, '3': None, '4': None, '5': None, '6': None, '7': None})
        self.assertEqual(list(foreground_apps), ["1", "2", "3", "4", "5", "6", "7"])

        del foreground_apps["3"]
        del foreground_apps["6"]
        self.assertEqual(list(foreground_apps), ["1", "2", "4", "5", "7"])

        foreground_apps["0"] = None
        self.assertEqual(list(foreground_apps), ["1", "2", "4", "5", "7", "0"])

    def test_next_dict(self):
        apps = ["1", "2", "3", "4", "5", "6", "7"]
        foreground_apps = {str(key): None for key in apps}

        self.assertEqual(list(foreground_apps).index("4"), 3)

        def next_app(a_list: list, app):
            try:
                i = a_list.index(app)
                ret = a_list[i + 1]
            except (ValueError, IndexError):
                return None
            else:
                return ret

        self.assertEqual(next_app(list(foreground_apps), "4"), "5")
        self.assertEqual(next_app(list(foreground_apps), "7"), None)
        self.assertEqual(next_app(list(foreground_apps), "8"), None)
        self.assertEqual(next_app(list(foreground_apps), "unknown"), None)
        self.assertEqual(next_app(list(foreground_apps), "1"), "2")
        self.assertEqual(next_app([], "1"), None)
        self.assertEqual(next_app([], "unknown"), None)
        self.assertEqual(next_app([], None), None)


if __name__ == '__main__':
    unittest.main()
