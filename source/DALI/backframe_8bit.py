from dali_interface import DaliFrame


class Backframe8Bit:
    LENGTH = 8

    def adr(self) -> str:
        return ""

    def cmd(self) -> str:
        return f"DATA 0x{self.frame_data:02X} = {self.frame_data:3} = {self.frame_data:08b}b"

    def data(self) -> str:
        return f"{self.frame_data:02X}"

    def __init__(self, frame: DaliFrame) -> None:
        self.frame_data = frame.data
