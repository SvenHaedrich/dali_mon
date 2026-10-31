from dali_interface import DaliFrame

from .backframe_8bit import Backframe8Bit
from .forward_frame_16bit import DeviceType, ForwardFrame16Bit
from .forward_frame_24bit import ForwardFrame24Bit
from .forward_frame_25bit import ForwardFrame25Bit
from .forward_frame_32bit import ForwardFrame32Bit
from .output_row import OutputRow


class UndefinedFrame:
    def __init__(self, frame: DaliFrame) -> None:
        self.frame = frame

    def output_row(self) -> OutputRow:
        return OutputRow(
            data=f"{self.frame.data:08X}",
            address="",
            command=f"--- UNDEFINED FRAMELENGTH {self.frame.length} BITS",
        )


class Decode:
    """Transforms a DALI frame into the row of the output.

    The decoder class is chosen by the length of the frame. Only the 16 bit forward
    frames depend on the frames before, by the device type of ENABLE DEVICE TYPE.
    """

    def __init__(self, frame: DaliFrame, device_type: int = DeviceType.NONE) -> None:
        # iec 62386-102 11.2: ENABLE DEVICE TYPE stays active until the next
        # command accepted by control gear, other frames don't end it
        self.next_device_type = device_type
        if frame.length == Backframe8Bit.LENGTH:
            self.dali_frame = Backframe8Bit(frame)
        elif frame.length == ForwardFrame16Bit.LENGTH:
            self.dali_frame = ForwardFrame16Bit(frame, device_type)
            if frame.address_byte == 0xC1:
                self.next_device_type = frame.opcode_byte
            else:
                self.next_device_type = DeviceType.NONE
        elif frame.length == ForwardFrame24Bit.LENGTH:
            self.dali_frame = ForwardFrame24Bit(frame)
        elif frame.length == ForwardFrame25Bit.LENGTH:
            self.dali_frame = ForwardFrame25Bit(frame)
        elif frame.length == ForwardFrame32Bit.LENGTH:
            self.dali_frame = ForwardFrame32Bit(frame)
        else:
            self.dali_frame = UndefinedFrame(frame)

    def output_row(self) -> OutputRow:
        return self.dali_frame.output_row()

    def get_next_device_type(self) -> int:
        return self.next_device_type
