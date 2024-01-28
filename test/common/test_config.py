import unittest
from touchpi.common.config import settings


class TestConfig(unittest.TestCase):
    def test_dynaconf(self):
        self.assertEqual(settings.testvar, 'foo')
        self.assertEqual(settings.core_environment, 'production')
        self.assertEqual(settings.core_sample_secret_name, 'prod-secret')


if __name__ == '__main__':
    unittest.main()
