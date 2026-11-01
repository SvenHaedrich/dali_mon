from dali_interface import DaliFrame

from .backframe_8bit import Backframe8Bit
from .decoded_frame import DecodedFrame
from .forward_frame_16bit import DeviceType, ForwardFrame16Bit
from .forward_frame_24bit import ForwardFrame24Bit
from .forward_frame_25bit import ForwardFrame25Bit
from .forward_frame_32bit import ForwardFrame32Bit


class UndefinedFrame(DecodedFrame):
    """A frame with a length that no decoder handles, only its length is shown."""

    def __init__(self, frame: DaliFrame) -> None:
        super().__init__(frame)
        self._command = f"--- UNDEFINED FRAMELENGTH {frame.length} BITS"


class Decode:
    """Decodes a DALI frame with the decoder for its length.

    dali_frame is the decoder, its getters give the texts of the frame.
    next_device_type is the device type to decode the next frame with: only
    16 bit forward frames depend on the frames before, by ENABLE DEVICE TYPE.
    """

    def __init__(self, frame: DaliFrame, device_type: int = DeviceType.NONE) -> None:
        # iec 62386-102 11.2: ENABLE DEVICE TYPE stays active until the next
        # command accepted by control gear, other frames don't end it
        self.next_device_type = device_type
        self.dali_frame: DecodedFrame
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
