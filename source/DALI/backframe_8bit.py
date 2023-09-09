class Backframe8Bit:
    LENGTH = 8

    def adr(self) -> str:
        return ""

    def cmd(self) -> str:
        return f"DATA 0x{self.data:02X} = {self.data:3} = {self.data:08b}b"

    def data(self) -> str:
        return f"{self.frame_data:02X}"

    def __init__(self, data: int) -> None:
        self.frame_data = data
