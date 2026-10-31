from dali_interface import DaliFrame

from .decoded_frame import IEC_62386_105, DecodedFrame

# frame_bytes[0] holds bits 31 to 24 of the frame, frame_bytes[3] bits 7 to 0


# see iec 62386-105 11.2 table 6 - standard commands
FIRMWARE_COMMANDS: dict[int, tuple[str, str, str]] = {
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


class ForwardFrame32Bit(DecodedFrame):
    """32 bit forward frame for the firmware transfer (IEC 62386-105).

    The data transfer commands BEGIN BLOCK and TRANSFER BLOCK DATA, and the
    firmware update commands to control gear or a control device.
    """

    LENGTH = 32
    DATA_DIGITS = 8

    def device_command(self) -> tuple[str, str, str]:
        opcode_byte = self.frame_bytes[2]
        return self.lookup(
            FIRMWARE_COMMANDS,
            opcode_byte,
            f"--- CODE 0x{opcode_byte:02X} = {opcode_byte} UNKNOWN FIRMWARE UPDATE COMMAND",
        )

    def build_address_string(self) -> bool:
        BROADCAST = 0x7F
        BROADCAST_UNADDRESSED = 0x7E
        if self.frame_bytes[0] & 0x01:
            # control device address space
            if self.frame_bytes[0] >> 1 == BROADCAST:
                self._address = "BC DEV"
                return True
            elif self.frame_bytes[0] >> 1 == BROADCAST_UNADDRESSED:
                self._address = "BC DEV UN"
                return True
            else:
                if not self.frame_bytes[0] & 0x80:
                    short_address = (self.frame_bytes[0] >> 1) & 0x3F
                    self._address = f"D{short_address:02}"
                    return True
        else:
            # control gear address space
            if self.frame_bytes[0] >> 1 == BROADCAST:
                self._address = "BC GEAR"
                return True
            elif self.frame_bytes[0] >> 1 == BROADCAST_UNADDRESSED:
                self._address = "BC GEAR UN"
                return True
            else:
                if not self.frame_bytes[0] & 0x80:
                    short_address = (self.frame_bytes[0] >> 1) & 0x3F
                    self._address = f"G{short_address:02}"
                    return True
            self._address = ""
        return False

    def data_bytes(self) -> str:
        first, second, third = self.frame_bytes[1:]
        return f"(0x{first:02X}, 0x{second:02X}, 0x{third:02X})"

    def data_transfer_commands(self):
        # see iec 62386-105 11.2 table 7 - data transfer commands
        BEGIN_BLOCK = 0xCB
        TRANSFER_BLOCK = 0xBD
        if self.frame_bytes[0] == BEGIN_BLOCK:
            self._address = ""
            self._command = "BEGIN BLOCK " + self.data_bytes()
            self._standard, self._reference = IEC_62386_105, "11.3.3.1"
            return True
        if self.frame_bytes[0] == TRANSFER_BLOCK:
            self._address = ""
            self._command = "TRANSFER BLOCK DATA " + self.data_bytes()
            self._standard, self._reference = IEC_62386_105, "11.3.3.2"
            return True
        return False

    def __init__(self, frame: DaliFrame) -> None:
        super().__init__(frame)
        self.frame_bytes = frame.data.to_bytes(4, byteorder="big")
        if self.data_transfer_commands():
            return
        if self.build_address_string() and self.frame_bytes[1] == 0xFB:
            self._command, self._standard, self._reference = self.device_command()
            return
        self._address = ""
        self._command = "---"
