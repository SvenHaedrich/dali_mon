import pytest
import logging

from DALI.dali_interface.dali_interface import DaliFrame, DaliStatus
from DALI.dali_interface.serial import DaliSerial
from DALI.dali_interface.hid import DaliUsb

serial_port = "/dev/ttyUSB0"
logger = logging.getLogger(__name__)
timeout_sec = 2


def test_8bit_frames():
    serial = DaliSerial(serial_port, start_receive=False)
    usb = DaliUsb()
    for data in range(0x100):
        send_frame = DaliFrame(length=8, data=data)
        serial.transmit(send_frame)
        result = usb.get(timeout_sec)
        assert result.length == send_frame.length
        assert result.data == send_frame.data
        assert result.status == DaliStatus.FRAME
    serial.close()
    usb.close()


@pytest.mark.parametrize(
    "data",
    [
        0x0000,
        0xFFFF,
        0x0001,
        0x0002,
        0x0004,
        0x0008,
        0x0010,
        0x0020,
        0x0040,
        0x0080,
        0x0100,
        0x0200,
        0x0400,
        0x0800,
        0x1000,
        0x2000,
        0x4000,
        0x8000,
        0xAAAA,
        0x5555,
    ],
)
def test_16bit_frame(data):
    serial = DaliSerial(serial_port, start_receive=False)
    usb = DaliUsb()
    send_frame = DaliFrame(length=16, data=data)
    serial.transmit(send_frame)
    result = usb.get(timeout_sec)
    assert result.length == send_frame.length
    assert result.data == send_frame.data
    assert result.status == DaliStatus.FRAME
    serial.close()
    usb.close()


# accepted framelengts:
# 8: backward frame
# 16: gear forward frame
# 17: Helvar
# 24: device forward frame
# 25: eDALI frame
# length above 25 are completely ignored
@pytest.mark.parametrize(
    "length,data",
    [
        (1, 0),
        (1, 1),
        (2, 0),
        (3, 0),
        (4, 0),
        (5, 0),
        (6, 0),
        (7, 0),
        (9, 0),
        (10, 0),
        (11, 0),
        (12, 0),
        (13, 0),
        (14, 0),
        (15, 0),
        (18, 0),
        (19, 0),
        (20, 0),
        (21, 0),
        (22, 0),
        (23, 0),
    ],
)
def test_invalid_frame_length(length, data):
    logger.setLevel(logging.DEBUG)
    serial = DaliSerial(serial_port, start_receive=False)
    usb = DaliUsb()
    send_frame = DaliFrame(length=length, data=data)
    serial.transmit(send_frame)
    result = usb.get(timeout_sec)
    assert result.status == DaliStatus.TIMING
    assert result.length == 0
    serial.close()
    usb.close()
