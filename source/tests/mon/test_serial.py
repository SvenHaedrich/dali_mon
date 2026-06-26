from DALI.dali_interface.dali_interface import DaliStatus, DaliSerial


def test_raw_from_string():
    input_string = "{00000000:08 000011}"
    result = DaliSerial.parse(input_string)
    assert result.timestamp == 0
    assert result.length == 0x8
    assert result.data == 0x11
    assert result.status == DaliStatus.FRAME
    input_string = "{00000001:10 0000FF00}"
    result = DaliSerial.parse(input_string)
    assert result.timestamp == 0.001
    assert result.length == 0x10
    assert result.data == 0xFF00
    assert result.status == DaliStatus.FRAME
    input_string = "{00000002:18 00123456}"
    result = DaliSerial.parse(input_string)
    assert result.timestamp == 0.002
    assert result.length == 0x18
    assert result.data == 0x123456
    assert result.status == DaliStatus.FRAME
    input_string = "{00000003:83 00123456}"
    result = DaliSerial.parse(input_string)
    assert result.timestamp == 0.003
    assert result.length == 0x83
    assert result.data == 0x123456
    assert result.status == DaliStatus.TIMING
    input_string = "{00000004:20 87654321}"
    result = DaliSerial.parse(input_string)
    assert result.timestamp == 0.004
    assert result.length == 0x20
    assert result.data == 0x87654321
    assert result.status == DaliStatus.FRAME
    input_string = "*** Booting Zephyr OS build v4.4.0-5197-g6f49860fc7a2 ***"
    result = DaliSerial.parse(input_string)
    assert result is None
    input_string = "aa{bb"
    result = DaliSerial.parse(input_string)
    assert result is None
    input_string = "aa}bb"
    result = DaliSerial.parse(input_string)
    assert result is None
    input_string = "aa}{bb"
    result = DaliSerial.parse(input_string)
    assert result is None
    input_string = "{aa}"
    result = DaliSerial.parse(input_string)
    assert result is None
    input_string = "{00000004:op 87654321}"
    result = DaliSerial.parse(input_string)
    assert result is None
