"""Apache log file parser"""

from collections import namedtuple
from datetime import datetime
from dateutil.parser import parse

def parse_line(line):
    """ Takes a line in the format "%a %l %u %t \"%r\" %>s %b %D", which relates to: 

        Remote IP | remote logname | remote user | time request received |
        "first line of request" | final status of request |
        size of response in bytes, excluding headers | time taken to serve request in microseconds

        and returns a parsed namedtuple of the information.

    """

    line = line.split()
    # Grouping the line explicitly like this should be less error
    # prone than using a regex, because the delimiters are consistent
    # in a way that the contents aren't
    try:
        line = [
            line[0],
            line[1],
            line[2],
            line[3].lstrip(b'[') + line[4].rstrip(b']'),
            line[5] + line[6] + line[7],
            line[8],
            line[9],
            line[10]
        ]
        # The colon between year and hour data in the log
        # stops parse being able to work, so we replace it
        line[3] = parse(line[3].decode('utf-8').replace(':', ' ', 1))

        ParsedLine = namedtuple('ParsedLine', [
            'IP',
            'remote_logname',
            'remote_user',
            'time_received',
            'first_line',
            'final_status',
            'response_size',
            'response_time'
        ])
        return ParsedLine(*line)
    except IndexError:
        return "I didn't understand your input"


def parse_file(file_path):
    """
    Takes a file path and returns:
    The number of successful requests per minute
    The number of error requests per minute
    The mean response time
    Megabytes sent per minute
    """

    with open(file_path, 'rb') as f:
        parsed_log = (parse_line(line) for line in f)
        successes = 0
        failures = 0
        response_total_time = 0
        megabytes_total = 0
        min_time = None
        max_time = None
        # accumulating this rather than evaluating the generator
        requests_served = 0
        for item in parsed_log:
            successes += 1 if item.final_status.startswith(b'2') else 0
            failures += 1 if item.final_status.startswith((b'4', b'5')) else 0
            response_total_time += int(item.response_time) if item.response_time.isdigit() else 0
            megabytes_total += int(item.response_size) if item.response_size.isdigit() else 0
            min_time = min(item.time_received, min_time) if min_time else item.time_received
            max_time = max(item.time_received, max_time) if max_time else item.time_received
            requests_served += 1

        minutes = (max_time - min_time).total_seconds() / 60
        successes_per_minute = successes / minutes
        failures_per_minute = failures / minutes
        mean_response_time = response_total_time / requests_served
        # taking 1,000,000 bytes as mega, see http://stackoverflow.com/a/2365124/1281947
        megabytes_per_minute = (megabytes_total / 1000000) / minutes
        Stats = namedtuple('Stats', [
            'successful_requests_per_minute',
            'failed_requests_per_minute',
            'mean_response_time',
            'megabytes_per_minute'
        ])
        return Stats(
            successes_per_minute,
            failures_per_minute,
            mean_response_time,
            megabytes_per_minute
        )
