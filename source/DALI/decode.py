from .backframe_8bit import Backframe8Bit
from .forward_frame_16bit import ForwardFrame16Bit, DeviceType
from .forward_frame_24bit import ForwardFrame24Bit
from .forward_frame_25bit import ForwardFrame25Bit
from .forward_frame_32bit import ForwardFrame32Bit


class Decode:
    ADDRESS_WIDTH = 14
    DATA_WIDTH = 8

    def __init__(self, length, data, device_type=DeviceType.NONE):
        self.length = length
        self.data = data
        self.result = ""
        self.active = device_type
        self.next_device_type = None

        if self.length == 16:
            address_byte = (self.data >> 8) & 0xFF
            if address_byte == 0xC1:
                self.next_device_type = self.data & 0xFF
            else:
                self.next_device_type = DeviceType.NONE
        else:
            self.next_device_type = DeviceType.NONE

    def get_next_device_type(self):
        return self.next_device_type

    def __str__(self):
        if self.length == 8:
            return f"{self.data:02X}".rjust(self.DATA_WIDTH)
        elif self.length == 16:
            return f"{self.data:04X}".rjust(self.DATA_WIDTH)
        elif self.length == 24:
            return f"{self.data:06X}".rjust(self.DATA_WIDTH)
        elif self.length == 25:
            return f"{self.data:07X}".rjust(self.DATA_WIDTH)
        else:
            return f"{self.data:08X}".rjust(self.DATA_WIDTH)

    def cmd(self):
        if self.length == 8:
            command = Backframe8Bit(self.data, self.ADDRESS_WIDTH)
        elif self.length == 16:
            command = ForwardFrame16Bit(self.data, self.active, self.ADDRESS_WIDTH)
        elif self.length == 24:
            command = ForwardFrame24Bit(self.data, self.ADDRESS_WIDTH)
        elif self.length == 25:
            command = ForwardFrame25Bit(self.data, self.ADDRESS_WIDTH)
        elif self.length == 32:
            command = ForwardFrame32Bit(self.data, self.ADDRESS_WIDTH)
        else:
            return (
                " " * self.ADDRESS_WIDTH
                + f"--- UNDEFINED FRAMELENGTH {self.length} BITS"
            )
        return command.address_string + command.command_string
