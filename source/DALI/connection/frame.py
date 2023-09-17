from typing import NamedTuple

from .status import DaliStatus


class DaliFrame(NamedTuple):
    timestamp: float = 0
    length: int = 0
    data: int = 0
    priority: int = 1
    send_twice: bool = False
    status: DaliStatus = DaliStatus(status=DaliStatus.OK)
