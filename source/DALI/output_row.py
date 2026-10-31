"""The result of decoding a DALI frame: one row of the output, every column a string."""

from typing import NamedTuple


class OutputRow(NamedTuple):
    """The columns of the output for one DALI frame.

    Frames without a reference to a standard leave standard and clause empty.
    """

    data: str
    address: str
    command: str
    standard: str = ""
    clause: str = ""
