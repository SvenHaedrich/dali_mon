from dali_interface import DaliFrame

from .output_row import IEC_62386_101, OutputRow


class Backframe8Bit:
    LENGTH = 8

    def __init__(self, frame: DaliFrame) -> None:
        self.frame = frame

    def output_row(self) -> OutputRow:
        value = self.frame.data
        return OutputRow(
            data=f"{value:02X}",
            address="",
            command=f"DATA 0x{value:02X} = {value:3} = {value:08b}b",
            standard=IEC_62386_101,
            clause="7.4.5",
        )
