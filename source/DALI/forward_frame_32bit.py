from dali_interface import DaliFrame

# frame_bytes[0] holds bits 31 to 24 of the frame, frame_bytes[3] bits 7 to 0


class ForwardFrame32Bit:
    LENGTH = 32

    def device_command(self) -> str:
        # see iec 62386-105 11.2 table 6 - standard commands
        code_dictionary = {
            0x00: "START FW TRANSFER",
            0x01: "RESTART FW",
            0x02: "ENABLE RESTART",
            0x03: "FINISH FW UPDATE",
            0x04: "CANCEL FW UPDATE",
            0x05: "QUERY FW UPDATE FEATURES",
            0x06: "QUERY FW RESTART ENABLED",
            0x07: "QUERY FW UPDATE RUNNING",
            0x08: "QUERY BLOCK FAULT",
        }
        opcode_byte = self.frame_bytes[2]
        return code_dictionary.get(
            opcode_byte,
            f"--- CODE 0x{opcode_byte:02X} = {opcode_byte} UNKNOWN FIRMWARE UPDATE COMMAND",
        )

    def build_address_string(self) -> bool:
        BROADCAST = 0x7F
        BROADCAST_UNADDRESSED = 0x7E
        if self.frame_bytes[0] & 0x01:
            # control device address space
            if self.frame_bytes[0] >> 1 == BROADCAST:
                self.address_string = "BC DEV"
                return True
            elif self.frame_bytes[0] >> 1 == BROADCAST_UNADDRESSED:
                self.address_string = "BC DEV UN"
                return True
            else:
                if not self.frame_bytes[0] & 0x80:
                    short_address = (self.frame_bytes[0] >> 1) & 0x3F
                    self.address_string = f"D{short_address:02}"
                    return True
        else:
            # control gear address space
            if self.frame_bytes[0] >> 1 == BROADCAST:
                self.address_string = "BC GEAR"
                return True
            elif self.frame_bytes[0] >> 1 == BROADCAST_UNADDRESSED:
                self.address_string = "BC GEAR UN"
                return True
            else:
                if not self.frame_bytes[0] & 0x80:
                    short_address = (self.frame_bytes[0] >> 1) & 0x3F
                    self.address_string = f"G{short_address:02}"
                    return True
            self.address_string = ""
        return False

    def data_bytes(self) -> str:
        first, second, third = self.frame_bytes[1:]
        return f"(0x{first:02x}, 0x{second:02x}, 0x{third:02x})"

    def data_transfer_commands(self):
        # see iec 62386-105 11.2 table 7 - data transfer commands
        BEGIN_BLOCK = 0xCB
        TRANSFER_BLOCK = 0xBD
        if self.frame_bytes[0] == BEGIN_BLOCK:
            self.address_string = ""
            self.command_string = "BEGIN BLOCK " + self.data_bytes()
            return True
        if self.frame_bytes[0] == TRANSFER_BLOCK:
            self.address_string = ""
            self.command_string = "TRANSFER BLOCK DATA " + self.data_bytes()
            return True
        return False

    def adr(self) -> str:
        return self.address_string

    def cmd(self) -> str:
        return self.command_string

    def data(self) -> str:
        return f"{self.frame_data:08X}"

    def __init__(self, frame: DaliFrame) -> None:
        self.frame_data = frame.data
        self.frame_bytes = frame.data.to_bytes(4, byteorder="big")
        if self.data_transfer_commands():
            return
        if self.build_address_string() and self.frame_bytes[1] == 0xFB:
            self.command_string = self.device_command()
            return
        self.address_string = ""
        self.command_string = "---"
        return
