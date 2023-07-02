import unittest

from segment import Segment
from units import units


class SegmentTest(unittest.TestCase):

    def test_min(self):
        segment = Segment(units[0])
        segment.values = [1, 12]
        self.assertEqual(segment.min(), 1)
        segment = Segment(units[1])
        segment.values = [12, 23]
        self.assertEqual(segment.min(), 12)

    def test_parse_range(self):
        segment = Segment(units[4])
        result = segment._parse_range('0')
        self.assertEqual(result, [0], 'Fail parsing a non range string')
        result = segment._parse_range('0-5')
        self.assertEqual(result, [0, 1, 2, 3, 4, 5], 'Fail parsing range')

    def test_apply_interval(self):
        segment = Segment(units[4])
        result = segment._apply_interval([2, 3, 4, 5, 6], 3)
        self.assertEqual(result, [2, 5])
