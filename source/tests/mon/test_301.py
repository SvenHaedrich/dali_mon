import pytest

from DALI.connection.frame import DaliFrame
from DALI.backframe_8bit import Backframe8Bit
from DALI.forward_frame_24bit import ForwardFrame24Bit
from DALI.decode import Decode, DeviceType


# TODO - make a complete test suite for all commands, for all instance addressing modes
# TODO - do this for 302, 303, 304 as well


def test_type_specific_commands():
    # undefined device
    test_frame = DaliFrame(length=ForwardFrame24Bit.LENGTH, data=0x010121)
    decoder = Decode(test_frame)
    data_str, adr, cmd = decoder.get_strings()
    target_adr = "D00,I01"
    target_cmd = "SET HOLD TIMER (DTR0) - TYPE 303"
    target_data = f"{test_frame.data:06X}"
    assert data_str == target_data
    assert adr == target_adr
    assert cmd == target_cmd

    test_frame = DaliFrame(length=ForwardFrame24Bit.LENGTH, data=0x01020A)
    decoder = Decode(test_frame)
    data_str, adr, cmd = decoder.get_strings()
    target_adr = "D00,I02"
    target_cmd = "QUERY SHORT TIMER - TYPE 301"
    target_data = f"{test_frame.data:06X}"
    assert data_str == target_data
    assert adr == target_adr
    assert cmd == target_cmd
