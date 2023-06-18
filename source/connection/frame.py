from .status import DaliStatus
from typing import NamedTuple


class DaliFrame(NamedTuple):
    timestamp: int = 0
    length: int = 0
    data: int = 0
    priority: int = 1
    send_twice: bool = False
    status: DaliStatus = DaliStatus(status=DaliStatus.OK)
