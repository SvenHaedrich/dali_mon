import pytest
import os
import sys

# locate the DALI module
here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, "../../source"))
import DALI
from connection.serial import DaliSerial
from connection.status import DaliStatus


def test_raw_from_string():
    input_string = "{00000000:08 000011}"
    frame = DaliSerial.parse(input_string)
    assert frame.timestamp == 0
    assert frame.length == 0x8
    assert frame.data == 0x11
    assert frame.status.status == DaliStatus.FRAME
    input_string = "{00000001:10 0000FF00}"
    frame = DaliSerial.parse(input_string)
    assert frame.timestamp == 0.001
    assert frame.length == 0x10
    assert frame.data == 0xFF00
    assert frame.status.status == DaliStatus.FRAME
    input_string = "{00000002:18 00123456}"
    frame = DaliSerial.parse(input_string)
    assert frame.timestamp == 0.002
    assert frame.length == 0x18
    assert frame.data == 0x123456
    assert frame.status.status == DaliStatus.FRAME
    input_string = "{00000003:83 00123456}"
    frame = DaliSerial.parse(input_string)
    assert frame.timestamp == 0.003
    assert frame.length == 0x83
    assert frame.data == 0x123456
    assert frame.status.status == DaliStatus.TIMING
    input_string = "{00000004:20 87654321}"
    frame = DaliSerial.parse(input_string)
    assert frame.timestamp == 0.004
    assert frame.length == 0x20
    assert frame.data == 0x87654321
    assert frame.status.status == DaliStatus.FRAME
