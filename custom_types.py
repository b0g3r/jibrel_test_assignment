"""
Store custom types for app.
"""
from typing import Optional, Tuple

START_REQUEST = 'StartRequest'
FINISH_REQUEST = 'FinishRequest'
BACKEND_CONNECT = 'BackendConnect'
BACKEND_OK = 'BackendOk'

EventType = Tuple[int, int, str, Optional[int], Optional[str]]
