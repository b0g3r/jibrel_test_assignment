"""
Entry point file.
"""
import argparse

import analyzer
import log_parser

arg_parser = argparse.ArgumentParser(description='Test assignment solution')
arg_parser.add_argument('filename', help='Full path to filename with extension')
args = arg_parser.parse_args()

with open(args.filename) as file_object:
    events = log_parser.log_file(file_object)
    failed, percentile_time = analyzer.calculate(events)
    print('Failed requests:', failed)  # noqa: T001
    print('95% percentile request time', percentile_time / 1000, 'ms')  # noqa: T001
