# Simple log file parser

This application takes a file path to an apache log file as an argument and returns statistics from it. The logs must be in the format:

    "%a %l %u %t \"%r\" %>s %b %D"

in order for the current implementation to work.

## Usage

From the project's root directory run

    python3 main.py /path/to/logfile

to start the application. It will take around two minutes to complete on a 100MB file.

## Testing


From the project's root directory run

    python3 -m unittest

to run the test suite.
