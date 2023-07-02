from typing import List, Union

from units import Unit


class Segment:
    """Creates an instance of Segment which is part of cron schedule.

    Attributes:
        unit object: The unit of measurement of time (see units.py).
    """
    def __init__(self, unit: Unit):
        self.unit = unit
        self.values = None

    def min(self) -> int:
        """
        :return: The smallest Segment value, which is the first element in list
        """
        return self.values[0]

    def max(self) -> int:
        """Returns largest Segment value, which is the last element in list """
        return self.values[-1]

    def out_of_range(self, values: List[int]) -> Union[int, None]:
        """Check for out of range validation. Returns failure value or None
        :param values: The values to test.
        """
        first = values[0]
        last = values[-1]
        if first < self.unit.min:
            return first
        elif last > self.unit.max:
            return last
        else:
            return None

    def parse_string(self, cron_segment: str) -> None:
        """Parses input string to segment range
        "," - denotes segment split
        "-" - denotes segment split range factor
        "/" - denote segment split step factor

        :param cron_segment: input string representing segment range. It will be converted as a range.
        :raises ValueError: Invalid value and Out of Range value
        """
        intervals_list = []  # Final list of list. Every sub-list will be a unit range

        # check for "," in input segment || Segment input split on "," needs to check for "-" : Range & "/" Step
        string_segments = cron_segment.split(',')
        for string_segment in string_segments:
            # Split in the case of step parameter
            range_step_string_segments = string_segment.split('/')

            if len(range_step_string_segments) > 2:
                raise ValueError(f'Invalid value {string_segment} in cron segment {cron_segment}')
            range_string = range_step_string_segments[0]
            # Range Calculation
            self.validate_range(range_string)

            if range_string == '*':       # * - represents all in that Segment Unit
                range_list = list(range(self.unit.min, self.unit.max + 1))
            else:
                # parse input string to handle subset range for Segment Unit (eg 1-5)
                range_list = self._parse_range(range_string)
                if self.out_of_range(range_list):
                    raise ValueError(f'Value out of range for {self.unit.name}')

            # Step Calculation and apply
            step = self._get_step(range_step_string_segments)
            self.validate_step(step)

            # Apply intervals to generate schedules
            interval_values = self._apply_interval(range_list, step)
            if not len(interval_values):
                raise ValueError(f'Empty intervals value {cron_segment}')
            intervals_list.append(interval_values)

        flattened_ranges_list = [item for sublist in intervals_list for item in sublist]
        flattened_ranges_list = list(dict.fromkeys(flattened_ranges_list))  # Remove eventual duplicates
        flattened_ranges_list.sort()
        self.values = flattened_ranges_list

    @staticmethod
    def validate_range(range_string):
        """Validate input range string"""

        if not range_string:
            raise ValueError(f'Invalid value {range_string}')

    def validate_step(self, step):
        """ Validate step value"""
        if step and step < 1:
            raise ValueError(f'Invalid interval step value {step} for {self.unit.name}')

    @staticmethod
    def _parse_range(unit_range: str) -> List[int]:
        """Parses segment range string. Example: input="5-10" output=[5, 6, 7, 8, 9, 10]
        :param unit_range: The range string.
        """
        sub_segments = unit_range.split('-')
        if len(sub_segments) == 1:
            try:
                value = int(sub_segments[0])
            except ValueError as exc:
                raise ValueError(f'Invalid value {unit_range} --> {exc}')
            return [value]
        elif len(sub_segments) == 2:
            try:
                min_value = int(sub_segments[0])
                max_value = int(sub_segments[1])
            except ValueError as exc:
                raise ValueError(f'Invalid min or max value from: {unit_range} --> {exc}')
            if max_value < min_value:
                raise ValueError(f'End range is less than Start range in {unit_range}')
            return [int_value for int_value in range(min_value, max_value + 1)]

    def _get_step(self, range_string_segments: List[str]) -> Union[None, int]:
        """Get the step segment of the segment string.

        :param range_string_segments: the segment string of the current range.
        :return step: parsed step.
        """
        step = None
        try:
            step = int(range_string_segments[1])
        except IndexError:
            pass
        except (ValueError, TypeError):
            raise ValueError(f'Invalid interval step value {step} for {self.unit.name}')

        return step

    @staticmethod
    def _apply_interval(values: List[int], step: int) -> List[int]:
        """Applies an interval step and returns all interval values

        :param values: A collection of numbers.
        :param step: The step value.
        """
        if step:
            min_value = values[0]
            values = [value for value in values if value % step == min_value % step or value == min_value]
        return values
