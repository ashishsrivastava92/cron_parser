import unittest

from cron import Cron
from tests.fixtures.invalid_crons import invalid_crons


class CronTestInvalid(unittest.TestCase):

    def test_from_string(self):
        for invalid_cron in invalid_crons:
            with self.subTest(range=invalid_cron):
                with self.assertRaises(invalid_cron['error'], msg=invalid_cron['message']):
                    cron = Cron()
                    cron.parse_string(invalid_cron['string'])
