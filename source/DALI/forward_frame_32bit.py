from bitstring import BitArray

# bit position translation
#
#  3322|2222||2222|1111||1111|11  ||    |      IEC docs
#  1098|7654||3210|9876||5432|1098||7654|3210
# -----+----++----+----++----+----++----+-----
#  0123|4567||8911|1111||1111|2222||2222|2233  BitArray index
#      |    ||  01|2345||6789|0123||4567|8901
#


class ForwardFrame32Bit:
    def device_command(self):
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
        opcode_byte = self.frame_bits[16:24].uint
        return code_dictionary.get(
            opcode_byte,
            f"--- CODE 0x{opcode_byte:02X} = {opcode_byte} UNKNOWN FIRMWARE UPDATE COMMAND",
        )

    def build_address_string(self):
        BROADCAST = 0x7F
        BROADCAST_UNADDRESSED = 0x7E
        if self.frame_bits[7]:
            # control device address space
            if self.frame_bits[:7].uint == BROADCAST:
                self.address_string = "BC DEV"
                return True
            elif self.frame_bits[:7].uint == BROADCAST_UNADDRESSED:
                self.address_string = "BC DEV UN"
                return True
            else:
                if not self.frame_bits[0]:
                    short_address = self.frame_bits[1:7].uint
                    self.address_string = f"D{short_address:02}"
                    return True
        else:
            # control gear address space
            if self.frame_bits[:7].uint == BROADCAST:
                self.address_string = "BC GEAR"
                return True
            elif self.frame_bits[:7].uint == BROADCAST_UNADDRESSED:
                self.address_string = "BC GEAR UN"
                return True
            else:
                if not self.frame_bits[0]:
                    short_address = self.frame_bits[1:7].uint
                    self.address_string = f"G{short_address:02}"
                    return True
            self.address_string = ""
        return False

    def data_bytes(self):
        return f"(0x{self.frame_bits[8:16]}, 0x{self.frame_bits[16:24]}, 0x{self.frame_bits[24:32]})"

    def data_transfer_commands(self):
        # see iec 62386-105 11.2 table 7 - data transfer commands
        BEGIN_BLOCK = 0xCB
        TRANSFER_BLOCK = 0xBD
        if self.frame_bits[:8].uint == BEGIN_BLOCK:
            self.address_string = " " * address_field_width
            self.command_string = "BEGIN BLOCK " + self.data_bytes()
            return True
        if self.frame_bits[:8].uint == TRANSFER_BLOCK:
            self.address_string = " " * address_field_width
            self.command_string = "TRANSFER BLOCK DATA " + self.data_bytes()
            return True
        return False

    def __init__(self, frame_data, address_field_width):
        self.frame_bits = BitArray(uint=frame_data, length=32)
        if self.data_transfer_commands():
            return
        if self.build_address_string():
            self.address_string = self.address_string.ljust(address_field_width)
            if self.frame_bits[8:16].uint == 0xFB:
                self.command_string = self.device_command()
                return
        self.command_string = f"--- 0x{self.frame_bits[8:16].uint:x}"
