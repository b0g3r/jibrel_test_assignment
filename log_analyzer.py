"""
Found and analyze requests by log events.
"""

import math
from collections import defaultdict
from typing import DefaultDict, Iterable, List, Optional, Set, Tuple

from custom_types import BACKEND_CONNECT, BACKEND_OK, FINISH_REQUEST, START_REQUEST, EventType


class Request:
    """
    Memory efficient Request class with few helpers.
    """

    __slots__ = ('started_at', 'finished_at', 'backend_groups')

    def __init__(self):
        self.started_at: Optional[int] = None
        self.finished_at: Optional[int] = None
        self.backend_groups: Set[Optional[int]] = set()

    @property
    def request_time(self) -> int:
        """
        Calculate requested time for request shrug.
        """
        if self.finished_at is None or self.started_at is None:
            raise ValueError('Not full logs file was provided')
        return self.finished_at - self.started_at

    @property
    def is_contains_fail(self) -> bool:
        """
        Returns True if one or more requests to backend was failed.
        """
        return bool(self.backend_groups)


def calculate(events: Iterable[EventType]) -> Tuple[int, int]:
    """
    Calculate sought values: count of failed requests and percentile time of requests.
    """
    requests = build_requests(events)
    failed = count_failed(requests)
    sorted_times = sorted(request.request_time for request in requests)
    percentile_time = calculate_percentile(sorted_times)
    return failed, percentile_time


def build_requests(events: Iterable[EventType]) -> Iterable[Request]:
    """
    Build request objects from events.

    Any request in event log has own id, and we just read the log and
    add all the found information about request in `Request` object.
    """
    requests_by_id: DefaultDict[int, Request] = defaultdict(Request)

    for timestamp, request_id, event_type, backend_id, _ in events:
        request = requests_by_id[request_id]
        if event_type == START_REQUEST:
            request.started_at = timestamp
        elif event_type == FINISH_REQUEST:
            request.finished_at = timestamp
        elif event_type == BACKEND_CONNECT:
            request.backend_groups.add(backend_id)
        elif event_type == BACKEND_OK:
            request.backend_groups.discard(backend_id)

    return requests_by_id.values()


def count_failed(requests: Iterable[Request]) -> int:
    """
    Counts failed requests.
    """
    return len([request for request in requests if request.is_contains_fail])


def calculate_percentile(times: List[int], percent=0.95) -> int:
    """
    Calculate percentile (by default 95%) for sorted `times`.

    If we cannot choose one index, we use average of two nearest.
    """
    index = (len(times) - 1) * percent

    if index.is_integer():
        percentile_time = times[int(index)]
    else:
        left_part = times[math.floor(index)]
        right_part = times[math.ceil(index)]
        percentile_time = round((left_part + right_part) / 2)

    return percentile_time
