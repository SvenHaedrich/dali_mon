from DALI.backframe_8bit import Backframe8Bit
from DALI.forward_frame_16bit import ForwardFrame16Bit, DeviceType
from DALI.forward_frame_24bit import ForwardFrame24Bit
from DALI.forward_frame_25bit import ForwardFrame25Bit

class Decode:
    def __init__(self, raw_frame, device_type=DeviceType.NONE):
        self.raw = raw_frame
        self.result = ""
        self.active = device_type
        self.next_device_type = None

        if self.raw.length == 16:
            address_byte = (self.raw.data >> 8) & 0xFF
            if address_byte == 0xC1:
                self.next_device_type = (self.raw.data & 0xFF)
            else:
                self.next_device_type = DeviceType.NONE
        else:
            self.next_device_type = DeviceType.NONE

    def get_next_device_type(self):
        return self.next_device_type

    def __str__(self,field_width=8):
        if self.raw.length == 8:
            return F"{self.raw.data:02X}".rjust(field_width)
        elif self.raw.length == 16:
            return F"{self.raw.data:04X}".rjust(field_width)
        elif self.raw.length == 24:
            return F"{self.raw.data:06X}".rjust(field_width)
        elif self.raw.length == 25:
            return F"{self.raw.data:07X}".rjust(field_width)
        else:
            return F"{self.raw.data:08X}".rjust(field_width)

    def cmd(self):
        if self.raw.length == 16:
            command = ForwardFrame16Bit(self.raw.data, self.active)
        elif self.raw.length == 24:
            command = ForwardFrame24Bit(self.raw.data)
        elif self.raw.length == 25:
            command = ForwardFrame25Bit(self.raw.data)
        elif self.raw.length == 8:
            command = Backframe8Bit(self.raw.data)
        else:
            return " "*10 + F"--- UNDEFINED FRAMELENGTH {self.raw.length} BITS"
        return command.address_string + command.command_string
