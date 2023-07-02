import unittest

from cron import Cron
from tests.fixtures.valid_crons import valid_cron_command_to_list


class CronTest(unittest.TestCase):

    def test_parse_string_breakdown(self):
        for valid_cron in valid_cron_command_to_list:
            with self.subTest(range=valid_cron):
                cron = Cron()
                cron.parse_string(valid_cron['in'])
                self.assertEqual(cron.parsed_cron_breakdown(), valid_cron['out'], 'Failed parsing cron string')
