"""
Contains a few util functions and generators for parsing logs and converting to basic python types.
"""
from typing import IO, Iterator

from custom_types import EventType


def log_file(file_object: IO[str]) -> Iterator[EventType]:
    """
    Generator for line-by-line log reading.

    We lazy read log file because it may be very large.
    We read it like text file, because log doesn't have long lines
    and chunk-reading isn't necessary.
    """
    for line in file_object:
        yield convert_line(line.strip())


def convert_line(log_line: str) -> EventType:
    """
    Convert log line to native python types.

    Uses asterisk unpacking for optional fields.
    """
    backend_id = None
    payload = None

    timestamp_raw, request_id_raw, request_type_raw, *optional_payload = log_line.split('\t')

    # little hack for DRY converting
    if len(optional_payload) > 0:
        backend_id = int(optional_payload[0])
    if len(optional_payload) > 1:
        payload = optional_payload[1]

    return int(timestamp_raw), int(request_id_raw), request_type_raw, backend_id, payload
