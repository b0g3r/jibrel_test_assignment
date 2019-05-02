"""
Entry point file.
"""
import argparse

import log_analyzer
import log_parser

arg_parser = argparse.ArgumentParser(
    description='Test assignment solution. Read the program documentation below.',
)
arg_parser.add_argument(
    'filename',
    help='Full path to logfile with extension',
    nargs='?',
    default='logs/002.in',
)
arg_parser.add_argument(
    '--throw',
    help='Turn on the throw mode: app throw out events with not required types for analyze.',
    action='store_true'
)
args = arg_parser.parse_args()

with open(args.filename) as file_object:
    events = log_parser.log_file(file_object, args.throw)
    failed, percentile_time = log_analyzer.calculate(events)
    print('Failed requests:', failed)  # noqa: T001
    print('95% percentile request time', percentile_time / 1000, 'ms')  # noqa: T001
