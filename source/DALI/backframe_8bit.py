from dali_interface import DaliFrame

from .decoded_frame import IEC_62386_101, DecodedFrame


class Backframe8Bit(DecodedFrame):
    """8 bit backward frame, the answer of control gear or a control device to a
    query (IEC 62386-101). It has no address, the command shows the answered value.
    """

    LENGTH = 8
    DATA_DIGITS = 2

    def __init__(self, frame: DaliFrame) -> None:
        super().__init__(frame)
        value = frame.data
        self._command = f"DATA 0x{value:02X} = {value:3} = {value:08b}b"
        self._standard = IEC_62386_101
        self._reference = "7.4.5"
