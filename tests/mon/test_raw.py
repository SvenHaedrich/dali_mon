import pytest
import os
import sys

# locate the DALI module
here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, "../../source"))

import DALI


@pytest.mark.parametrize(
    "code,message",
    [(DALI.DALIError.OK, "OK"), (DALI.DALIError.FRAME, "ERROR: INVALID FRAME"), (-1, "UNDEFINED ERROR CODE (-1)")],
)
def test_error_codes(code, message):
    error = DALI.DALIError(code)
    error_string = error.__str__()
    assert error_string == message


def test_raw_from_string():
    frame = DALI.Raw_Frame()
    input_string = "{00000000-08 000011}".encode("utf-8")
    frame.from_line(input_string)
    assert frame.length == 0x8
    assert frame.data == 0x11
    assert frame.type == DALI.Raw_Frame.VALID
    assert frame.timestamp == 0
    input_string = "{00000001-10 0000FF00}".encode("utf-8")
    frame.from_line(input_string)
    assert frame.length == 0x10
    assert frame.data == 0xFF00
    assert frame.type == DALI.Raw_Frame.VALID
    assert frame.timestamp == 0.001
    input_string = "{00000002-18 00123456}".encode("utf-8")
    frame.from_line(input_string)
    assert frame.length == 0x18
    assert frame.data == 0x123456
    assert frame.type == DALI.Raw_Frame.VALID
    assert frame.timestamp == 0.002
    input_string = "{00000003*01 00123456}".encode("utf-8")
    frame.from_line(input_string)
    assert frame.length == 0x01
    assert frame.data == 0x123456
    assert frame.type == DALI.Raw_Frame.ERROR
    assert frame.timestamp == 0.003
