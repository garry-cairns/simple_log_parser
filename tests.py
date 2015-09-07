#!/usr/bin/python3
"""Unit tests for log parser"""

from unittest import TestCase
import datetime
from collections import namedtuple
from parser.line_parser import parse_line

class TestLineParsing(TestCase):
    """Tests each component of the parsing chain"""

    def test_parses_line(self):
        """
        Takes an example line and return a parsed line.
        """

        raw_line = """127.0.0.1 - - [30/Mar/2015:05:04:20 +0100] "GET /render/?from=-11minutes&until=-5mins&uniq=1427688307512&format=json&target=alias%28movingAverage%28divideSeries%28sum%28nonNegativeDerivative%28collector.uk1.rou.*rou*.svc.*.RoutesService.routedate.total.processingLatency.totalMillis.count%29%29%2Csum%28nonNegativeDerivative%28collector.uk1.rou.*rou*.svc.*.RoutesService.routedate.total.processingLatency.totalCalls.count%29%29%29%2C%275minutes%27%29%2C%22Latency%22%29 HTTP/1.1" 200 157 165169"""
        self.assertEqual(
            parse_line(raw_line),
            ParsedLine(
                IP='127.0.0.1',
                remote_logname='-',
                remote_user='-',
                time_received='[30/Mar/2015:05:04:20 +0100]',
                first_line="GET /render/?from=-11minutes&until=-5mins&uniq=1427688307512&format=json&target=alias%28movingAverage%28divideSeries%28sum%28nonNegativeDerivative%28collector.uk1.rou.*rou*.svc.*.RoutesService.routedate.total.processingLatency.totalMillis.count%29%29%2Csum%28nonNegativeDerivative%28collector.uk1.rou.*rou*.svc.*.RoutesService.routedate.total.processingLatency.totalCalls.count%29%29%29%2C%275minutes%27%29%2C%22Latency%22%29 HTTP/1.1",
                final_status='200',
                response_size=157,
                response_time=165169
            )
        )


