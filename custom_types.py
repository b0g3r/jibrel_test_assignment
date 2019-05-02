"""
Store custom types for app.
"""
from typing import Optional, Tuple

START_REQUEST = 'StartRequest'
FINISH_REQUEST = 'FinishRequest'
BACKEND_CONNECT = 'BackendConnect'
BACKEND_OK = 'BackendOk'

REQUIRED_TYPES = {START_REQUEST, FINISH_REQUEST, BACKEND_OK, BACKEND_CONNECT}

EventType = Tuple[int, int, str, Optional[int], Optional[str]]
