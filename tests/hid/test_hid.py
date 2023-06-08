import pytest
import os
import sys
import logging

# locate some of the project modules
here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, "../../source"))

from connection import serial as dali_serial
from connection import hid as dali_hid
import DALI


serial_port = "/dev/ttyUSB0"
logger = logging.getLogger(__name__)


def test_8bit_frames():
    serial = dali_serial.DaliSerial(serial_port)
    usb = dali_hid.DaliUsb()
    usb.start_receive()
    for data in range(0x100):
        serial.transmit(8, data)
        result = usb.get_next()
        assert usb.length == 8
        assert usb.data == data
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
    serial = dali_serial.DaliSerial(serial_port)
    usb = dali_hid.DaliUsb()
    usb.start_receive()
    frame = DALI.Raw_Frame(length=16, data=data)
    serial.write(frame)
    readback = usb.read_raw_frame()
    assert frame == readback, f"unexpected result: {readback}"
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
    serial = dali_serial.DaliSerial(serial_port)
    usb = dali_hid.DaliUsb()
    usb.start_receive()
    frame = DALI.Raw_Frame(length=length, data=data)
    serial.write(frame)
    readback = usb.read_raw_frame()
    assert readback.type == DALI.Raw_Frame.ERROR
    assert readback.length == DALI.DALIError.FRAME
    serial.close()
    usb.close()
