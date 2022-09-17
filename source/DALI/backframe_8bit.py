class Backframe8Bit:

    def __init__(self, frame, address_field_width=10):
        self.address_string = " " * address_field_width
        self.command_string = F"DATA 0x{frame:02X} = {frame:3} = {frame:08b}b"