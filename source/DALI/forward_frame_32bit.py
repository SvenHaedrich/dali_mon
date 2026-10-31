from dali_interface import DaliFrame

from .output_row import IEC_62386_105, OutputRow

# frame_bytes[0] holds bits 31 to 24 of the frame, frame_bytes[3] bits 7 to 0


class ForwardFrame32Bit:
    LENGTH = 32

    def device_command(self) -> tuple[str, str, str]:
        # see iec 62386-105 11.2 table 6 - standard commands
        code_dictionary = {
            0x00: ("START FW TRANSFER", IEC_62386_105, "11.3.2.1"),
            0x01: ("RESTART FW", IEC_62386_105, "11.3.2.8"),
            0x02: ("ENABLE RESTART", IEC_62386_105, "11.3.2.7"),
            0x03: ("FINISH FW UPDATE", IEC_62386_105, "11.3.2.2"),
            0x04: ("CANCEL FW UPDATE", IEC_62386_105, "11.3.2.6"),
            0x05: ("QUERY FW UPDATE FEATURES", IEC_62386_105, "11.3.2.3"),
            0x06: ("QUERY FW RESTART ENABLED", IEC_62386_105, "11.3.2.9"),
            0x07: ("QUERY FW UPDATE RUNNING", IEC_62386_105, "11.3.2.4"),
            0x08: ("QUERY BLOCK FAULT", IEC_62386_105, "11.3.2.5"),
        }
        opcode_byte = self.frame_bytes[2]
        return OutputRow.lookup(
            code_dictionary,
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
            self.standard, self.clause = IEC_62386_105, "11.3.3.1"
            return True
        if self.frame_bytes[0] == TRANSFER_BLOCK:
            self.address_string = ""
            self.command_string = "TRANSFER BLOCK DATA " + self.data_bytes()
            self.standard, self.clause = IEC_62386_105, "11.3.3.2"
            return True
        return False

    def __init__(self, frame: DaliFrame) -> None:
        self.frame = frame
        self.frame_bytes = frame.data.to_bytes(4, byteorder="big")
        self.clause = ""
        self.standard = ""
        if self.data_transfer_commands():
            return
        if self.build_address_string() and self.frame_bytes[1] == 0xFB:
            self.command_string, self.standard, self.clause = self.device_command()
            return
        self.address_string = ""
        self.command_string = "---"

    def output_row(self) -> OutputRow:
        return OutputRow(
            f"{self.frame.data:08X}",
            self.address_string,
            self.command_string,
            self.standard,
            self.clause,
        )
