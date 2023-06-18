import pytest
import logging

from connection.status import DaliStatus
from connection.serial import DaliSerial
from connection.hid import DaliUsb
from connection.frame import DaliFrame

serial_port = "/dev/ttyUSB0"
logger = logging.getLogger(__name__)
timeout_sec = 2


def test_8bit_frames():
    serial = DaliSerial(serial_port)
    usb = DaliUsb()
    usb.start_receive()
    for data in range(0x100):
        send_frame = DaliFrame(length=8, data=data)
        serial.transmit(send_frame)
        usb.get_next(timeout_sec)
        assert usb.rx_frame.length == send_frame.length
        assert usb.rx_frame.data == send_frame.data
        assert usb.rx_frame.status.status == DaliStatus.FRAME
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
    serial = DaliSerial(serial_port)
    usb = DaliUsb()
    usb.start_receive()
    send_frame = DaliFrame(length=16, data=data)
    serial.transmit(send_frame)
    usb.get_next(timeout_sec)
    assert usb.rx_frame.length == send_frame.length
    assert usb.rx_frame.data == send_frame.data
    assert usb.rx_frame.status.status == DaliStatus.FRAME
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
    serial = DaliSerial(serial_port)
    usb = DaliUsb()
    usb.start_receive()
    send_frame = DaliFrame(length=length, data=data)
    serial.transmit(send_frame)
    usb.get_next(timeout_sec)
    assert usb.rx_frame.status.status == DaliStatus.TIMING
    assert usb.rx_frame.length == 0
    serial.close()
    usb.close()
