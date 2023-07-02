from __future__ import annotations

import uuid

from typing import List, Dict, Union

from command import Command
from segment import Segment
from units import units


class Cron:
    """Creates a Cron schedule instance, along with command.

    :param:
        cron_string: input cron string
    """
    def __init__(self, cli_string: str = None) -> None:
        self.id = uuid.uuid4()
        self.segments = None
        self.command = None
        if cli_string:
            self.parse_string(cli_string)

    def get_command(self):
        return self.command

    @staticmethod
    def validate_cron_input_to_parse(cron_string) -> List[str]:
        if type(cron_string) != str:
            raise TypeError('Invalid cron string')
        cron_input = cron_string.strip().split()
        if len(cron_input) != 6:
            raise ValueError("Invalid CLI input")
        segments_len = len(cron_input[:5])
        if segments_len != 5:
            raise ValueError("Invalid cron string format")
        return cron_input

    def parse_string(self, cron_string: str) -> Cron:
        """Parses a cli_input - sample */15 0 1,15 * 1-5 /usr/bin/find

        :param cron_string: (str) The cron string to parse. It has to be made up 5 segments.
        :raises ValueError: Incorrect length of the cron string.
        """
        cron_input = self.validate_cron_input_to_parse(cron_string)
        self.segments = cron_input[:5]
        self.command = Command(cron_input[-1])
        if len(self.segments) != 5:
            raise ValueError("Invalid cron string format")
        cron_segments = []
        for item, unit in zip(self.segments, units):
            segment = Segment(unit)
            segment.parse_string(item)
            cron_segments.append(segment)

        self.segments = cron_segments
        return self

    def parsed_cron_breakdown(self) -> Dict[str:List[Union[int, str]]]:
        """Returns the cron schedule in units breakdown

        :return: Cron breakdown per segment
        :raises LookupError: Empty Cron object.
        """
        if not self.segments:
            raise LookupError('No schedule')
        schedule_data = dict()
        for segment in self.segments:
            schedule_data[segment.unit.name] = segment.values
        schedule_data['command'] = self.command.command
        return schedule_data
