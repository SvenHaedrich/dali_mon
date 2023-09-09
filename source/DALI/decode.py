from typing import Tuple

from .connection.frame import DaliFrame
from .backframe_8bit import Backframe8Bit
from .forward_frame_16bit import ForwardFrame16Bit, DeviceType
from .forward_frame_24bit import ForwardFrame24Bit
from .forward_frame_25bit import ForwardFrame25Bit
from .forward_frame_32bit import ForwardFrame32Bit


class UndefinedFrame:
    def __init__(self, data: int, length: int) -> None:
        self.data_frame = data
        self.length = length

    def adr(self) -> str:
        return ""

    def cmd(self) -> str:
        return f"--- UNDEFINED FRAMELENGTH {self.length} BITS"

    def data(self) -> str:
        return f"{self.data_frame:08X}"


class Decode:
    def get_strings(self) -> Tuple[str, str, str]:
        return self.dali_frame.data(), self.dali_frame.adr(), self.dali_frame.cmd()

    def __init__(
        self, frame: DaliFrame, device_type: DeviceType = DeviceType.NONE
    ) -> None:
        self.next_device_type = DeviceType.NONE
        if frame.length == Backframe8Bit.LENGTH:
            self.dali_frame = Backframe8Bit(frame.data)
        elif frame.length == ForwardFrame16Bit.LENGTH:
            self.dali_frame = ForwardFrame16Bit(frame.data, device_type)
            address_byte = (frame.data >> 8) & 0xFF
            if address_byte == 0xC1:
                self.next_device_type = frame.data & 0xFF
            else:
                self.next_device_type = DeviceType.NONE
        elif frame.length == ForwardFrame24Bit.LENGTH:
            self.dali_frame = ForwardFrame24Bit(frame.data)
        elif frame.length == ForwardFrame25Bit.LENGTH:
            self.dali_frame = ForwardFrame25Bit(frame.data)
        elif frame.length == ForwardFrame32Bit.LENGTH:
            self.dali_frame = ForwardFrame32Bit(frma.data)
        else:
            self.dali_frame = UndefinedFrame(frame.data, frame.length)

    def get_next_device_type(self) -> DeviceType:
        return self.next_device_type
