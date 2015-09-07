#!/usr/bin/python3
"""Unit tests for log parser"""

from unittest import TestCase
from collections import namedtuple
from dateutil.parser import parse
from parser.line_parser import parse_line, parse_lines

class TestLineParsing(TestCase):
    """Tests each component of the parsing chain"""

    def test_parses_line(self):
        """
        Takes an example line and returns a parsed line.
        """

        raw_line = b"""127.0.0.1 - - [30/Mar/2015:05:04:20 +0100] "GET /render/ HTTP/1.1" 200 157 165169"""
        self.assertEqual(
            parse_line(raw_line),
            (
                b'127.0.0.1',
                b'-',
                b'-',
                parse('30/Mar/2015 05:04:20 +0100'),
                b'"GET/render/HTTP/1.1"',
                b'200',
                b'157',
                b'165169'
            ),
        )


    def test_parses_lines(self):
        """
        Takes example input and returns statistics.
        """

        raw_lines = [
            b"""127.0.0.1 - - [30/Mar/2015:05:04:20 +0100] "GET /render/ HTTP/1.1" 200 100 100000""",
            b"""127.0.0.1 - - [30/Mar/2015:05:04:20 +0100] "GET /render/ HTTP/1.1" 500 100 100000""",
            b"""127.0.0.1 - - [30/Mar/2015:05:05:20 +0100] "GET /render/ HTTP/1.1" 200 100 100000""",
        ]
        # we wrap our known input in a generator, to mimic the way data is passed to parse_lines
        # by the get_file function
        raw_lines = (parse_line(line) for line in raw_lines)
        self.assertEqual(
            parse_lines(raw_lines),
            (2.0, 1.0, 100000.0, 0.0003)
        )