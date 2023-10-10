import pytest

from DALI.dali_interface.source.frame import DaliFrame
from DALI.forward_frame_16bit import ForwardFrame16Bit
from DALI.decode import Decode, DeviceType


def build_dt6_frame_and_test(test_data: int, target_adr: str, target_cmd: str) -> None:
    test_frame = DaliFrame(length=ForwardFrame16Bit.LENGTH, data=test_data)
    target_data = f"{test_data:04X}"
    data_str, adr, cmd = Decode(test_frame, DeviceType.LED).get_strings()
    assert data_str == target_data
    assert adr == target_adr
    assert cmd[: len(target_cmd)] == target_cmd


# refer to iec62386 207 Table 6
@pytest.mark.parametrize(
    "target_cmd,opcode",
    [
        ("REFERENCE SYSTEM POWER", 0xE0),
        ("SELECT DIMMING CURVE (DTR0)", 0xE3),
        ("SET FAST FADE TIME (DTR0)", 0xE4),
        ("QUERY CONTROL GEAR TYPE", 0xED),
        ("QUERY DIMMING CURVE", 0xEE),
        ("QUERY FEATURES", 0xF0),
        ("QUERY LOAD DECREASE", 0xF4),
        ("QUERY LOAD INCREASE", 0xF5),
        ("QUERY THERMAL SHUTDOWN", 0xF7),
        ("QUERY THERMAL OVERLOAD", 0xF8),
        ("QUERY REFERENCE RUNNING", 0xF9),
        ("QUERY REFERENCE MEASUREMENT FAILED", 0xFA),
        ("QUERY FAST FADE TIME", 0xFD),
        ("QUERY MIN FAST FADE TIME", 0xFE),
        ("QUERY EXTENDED VERSION NUMBER", 0xFF),
    ],
)
def test_dt6_command(target_cmd, opcode):
    # broadcast
    test_data = 0xFF00 + opcode
    build_dt6_frame_and_test(test_data, "BC GEAR", target_cmd)
    # broadcast unadressed
    test_data = 0xFD00 + opcode
    build_dt6_frame_and_test(test_data, "BC GEAR UN", target_cmd)
    # short address
    for short_address in range(0, 0x40):
        test_data = 0x0100 + (short_address << 9) + opcode
        target_adr = f"G{short_address:02}"
        build_dt6_frame_and_test(test_data, target_adr, target_cmd)
    # group address
    for group_address in range(0, 0x10):
        test_data = 0x8100 + (group_address << 9) + opcode
        target_adr = f"GG{group_address:02}"
        build_dt6_frame_and_test(test_data, target_adr, target_cmd)


@pytest.mark.parametrize(
    "opcode",
    [
        0xE1,
        0xE2,
        0xE5,
        0xE6,
        0xE7,
        0xE8,
        0xE9,
        0xEA,
        0xEB,
        0xEC,
        0xEF,
        0xF2,
        0xF3,
        0xF6,
        0xFB,
        0xFC,
    ],
)
def test_dt6_undefined_codes(opcode):
    # broadcast
    test_data = 0xFF00 + opcode
    build_dt6_frame_and_test(test_data, "BC GEAR", "---")
    # broadcast unadressed
    test_data = 0xFD00 + opcode
    build_dt6_frame_and_test(test_data, "BC GEAR UN", "---")
    # short address
    for short_address in range(0, 0x40):
        test_data = 0x0100 + (short_address << 9) + opcode
        target_adr = f"G{short_address:02}"
        build_dt6_frame_and_test(test_data, target_adr, "---")
    # group address
    for group_address in range(0, 0x10):
        test_data = 0x8100 + (group_address << 9) + opcode
        target_adr = f"GG{group_address:02}"
        build_dt6_frame_and_test(test_data, target_adr, "---")
