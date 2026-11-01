import pytest
from dali_interface import DaliFrame

from DALI.decode import Decode
from DALI.forward_frame_25bit import DeviceClass, ForwardFrame25Bit


def edali_frame(device_class: int, address_byte: int, opcode: int) -> DaliFrame:
    # class in bits 20 to 17, address in bits 16 to 9, opcode in bits 7 to 0
    data = (device_class << 17) | (address_byte << 9) | opcode
    return DaliFrame(length=ForwardFrame25Bit.LENGTH, data=data)


@pytest.mark.parametrize("device_class", [DeviceClass.SENSOR, DeviceClass.INPUT])
@pytest.mark.parametrize(
    "opcode,command",
    [
        (0x53, "START PARAMETER DOWNLOAD"),
        (0x54, "STOP PARAMETER DOWNLOAD"),
    ],
)
def test_parameter_download(device_class, opcode, command):
    decoded = Decode(edali_frame(device_class, 0x03, opcode)).dali_frame
    assert decoded.address() == f"C{device_class} E01"
    assert decoded.command() == command
    assert decoded.standard() == "eDALI"
