#!/usr/bin/python3
"""Entrypoint for logfile parser"""

import sys
import os.path
from parser.line_parser import get_file

def main(*args):
    """
    Takes a file path passed in by the user and processes it, returning statistics.
    """

    if len(sys.argv) == 1:
        sys.exit('Please supply an absolute file path')
    if len(sys.argv) > 2:
        sys.exit('Received an unexpected argument')

    if not os.path.isfile(sys.argv[1]):
        sys.exit(' '.join([
            'File',
            sys.argv[1],
            'does not exist'
        ]))


    print(get_file(sys.argv[1]))
    sys.exit(1) 


if __name__ == '__main__':
    sys.exit(main())