import unittest
import touchpi.common.shared
from test.common.test_data_helper1 import SimulateDesktop
from test.common.test_data_helper2 import SimulateApp


class TestSharedData(unittest.TestCase):

    def test_direct_call(self):
        self.assertEqual(touchpi.common.shared.data.get("_core_", "window"), None)
        self.assertEqual(touchpi.common.shared.data.get("_core_", "rc"), 0)
        self.assertRaises(KeyError, touchpi.common.shared.data.get, "_core_", "test")

    def test_desktop_call(self):
        self.assertEqual(touchpi.common.shared.data.get("_core_", "window"), None)
        self.assertEqual(touchpi.common.shared.data.get("_core_", "rc"), 0)
        self.assertRaises(KeyError, touchpi.common.shared.data.get, "_core_", "test")

        desktop = SimulateDesktop("test_desktop_call")
        desktop.insert_test_data("test", "test1")
        self.assertEqual(desktop.get_test_data("test"), "test1")
        desktop.delete_test_data("test")
        self.assertRaises(KeyError, desktop.get_test_data, "test")

    def test_app_call(self):
        self.assertEqual(touchpi.common.shared.data.get("_core_", "window"), None)
        self.assertEqual(touchpi.common.shared.data.get("_core_", "rc"), 0)
        self.assertRaises(KeyError, touchpi.common.shared.data.get, "_core_", "test")

        app = SimulateApp("test_app_call")
        app.insert_test_data("test", "1")
        self.assertEqual(app.get_test_data("test"), "1")
        app.delete_test_data("test")
        self.assertRaises(KeyError, app.get_test_data, "test")

    def test_mixed_call(self):
        self.assertEqual(touchpi.common.shared.data.get("_core_", "window"), None)
        self.assertEqual(touchpi.common.shared.data.get("_core_", "rc"), 0)
        self.assertRaises(KeyError, touchpi.common.shared.data.get, "_core_", "test")

        desktop = SimulateDesktop("test_mixed_call")
        app = SimulateApp("test_mixed_call")
        desktop.insert_test_data("test", "test1")
        self.assertEqual(desktop.get_test_data("test"), "test1")
        app.insert_test_data("test", "1")
        self.assertEqual(app.get_test_data("test"), "1")
        self.assertEqual(desktop.get_test_data("test"), "1")
        desktop.insert_test_data("test", "test1")
        self.assertEqual(desktop.get_test_data("test"), "test1")
        self.assertEqual(app.get_test_data("test"), "test1")
        app.delete_test_data("test")
        self.assertRaises(KeyError, app.get_test_data, "test")
        self.assertRaises(KeyError, desktop.delete_test_data, "test")

    def test_cascade_call(self):
        self.assertEqual(touchpi.common.shared.data.get("_core_", "window"), None)
        self.assertEqual(touchpi.common.shared.data.get("_core_", "rc"), 0)
        self.assertRaises(KeyError, touchpi.common.shared.data.get, "_core_", "test")

        desktop = SimulateDesktop("test_cascade_call")
        desktop.load_app("test_cascade_call")
        desktop.insert_test_data("test", "test1")
        self.assertEqual(desktop.get_test_data("test"), "test1")
        desktop.app.insert_test_data("test", "X")
        self.assertEqual(desktop.app.get_test_data("test"), "X")
        self.assertEqual(desktop.get_test_data("test"), "X")
        desktop.insert_test_data("test", "test1")
        self.assertEqual(desktop.get_test_data("test"), "test1")
        self.assertEqual(desktop.app.get_test_data("test"), "test1")
        desktop.delete_test_data("test")
        self.assertRaises(KeyError, desktop.get_test_data, "test")
        self.assertRaises(KeyError, desktop.app.get_test_data, "test")


if __name__ == '__main__':
    unittest.main()
