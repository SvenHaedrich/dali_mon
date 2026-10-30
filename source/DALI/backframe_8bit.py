from dali_interface import DaliFrame

from .reference import IEC_62386_101


class Backframe8Bit:
    LENGTH = 8

    def adr(self) -> str:
        return ""

    def cmd(self) -> str:
        return f"DATA 0x{self.frame.data:02X} = {self.frame.data:3} = {self.frame.data:08b}b"

    def data(self) -> str:
        return f"{self.frame.data:02X}"

    def __init__(self, frame: DaliFrame) -> None:
        self.frame = frame
        self.clause = "7.4.5"
        self.standard = IEC_62386_101
