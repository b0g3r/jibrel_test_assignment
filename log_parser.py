"""
Contains a few util functions and generators for parsing logs and converting to basic python types.
"""
from typing import IO, Iterator, Optional

from custom_types import EventType, REQUIRED_TYPES


def log_file(file_object: IO[str], throw: bool) -> Iterator[EventType]:
    """
    Generator for line-by-line log reading.

    We lazy read log file because it may be very large.
    We read it like text file, because log doesn't have long lines
    and chunk-reading isn't necessary.
    """
    for line in file_object:
        event = convert_line(line.strip(), throw=throw)
        if event is not None:  # filter for throw mode
            yield event


def convert_line(log_line: str, throw: bool) -> Optional[EventType]:
    """
    Convert log line to native python types.

    Uses asterisk unpacking for optional fields.
    """
    backend_id = None
    payload = None

    timestamp_raw, request_id_raw, event_type, *optional_payload = log_line.split('\t')

    # if throw mode is on we just throw events with not interested type
    if throw and event_type not in REQUIRED_TYPES:
        return None

    # little hack for DRY converting
    if len(optional_payload) > 0:
        backend_id = int(optional_payload[0])
    if len(optional_payload) > 1:
        payload = optional_payload[1]

    return int(timestamp_raw), int(request_id_raw), event_type, backend_id, payload
