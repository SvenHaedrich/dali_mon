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
    input_string = "{00000000:08 000011}".encode("utf-8")
    result = DaliSerial.parse(input_string)
    assert result[0] == 0
    assert result[1] == False
    assert result[2] == 0x8
    assert result[3] == 0x11
    input_string = "{00000001:10 0000FF00}".encode("utf-8")
    result = DaliSerial.parse(input_string)
    assert result[0] == 0.001
    assert result[1] == False
    assert result[2] == 0x10
    assert result[3] == 0xFF00
    input_string = "{00000002:18 00123456}".encode("utf-8")
    result = DaliSerial.parse(input_string)
    assert result[0] == 0.002
    assert result[1] == False
    assert result[2] == 0x18
    assert result[3] == 0x123456
    input_string = "{00000003:83 00123456}".encode("utf-8")
    result = DaliSerial.parse(input_string)
    assert result[0] == 0.003
    assert result[1] == False
    assert result[2] == 0x83
    assert result[3] == 0x123456
    input_string = "{00000004:20 87654321}".encode("utf-8")
    result = DaliSerial.parse(input_string)
    assert result[0] == 0.004
    assert result[1] == False
    assert result[2] == 0x20
    assert result[3] == 0x87654321
