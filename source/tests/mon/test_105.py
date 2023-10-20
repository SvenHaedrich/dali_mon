import pytest

from DALI.dali_interface.dali_interface import DaliFrame
from DALI.forward_frame_32bit import ForwardFrame32Bit
from DALI.decode import Decode


def build_firmware_frame(
    address_byte: int = 0,
    opcode_byte_1: int = 0,
    opcode_byte_2: int = 0,
    opcode_byte_3: int = 0,
) -> int:
    data = address_byte & 0xFF
    data = (data << 8) + (opcode_byte_1 & 0xFF)
    data = (data << 8) + (opcode_byte_2 & 0xFF)
    data = (data << 8) + (opcode_byte_3 & 0xFF)
    return data


def build_32bit_frame_and_test(
    test_data: int, target_adr: str, target_cmd: str
) -> None:
    test_frame = DaliFrame(length=ForwardFrame32Bit.LENGTH, data=test_data)
    target_data = f"{test_data:08X}"
    data_str, adr, cmd = Decode(test_frame).get_strings()
    assert data_str == target_data
    assert adr == target_adr
    assert cmd[: len(target_cmd)] == target_cmd


def test_block_commands():
    test_data = build_firmware_frame(0xCB, 0x01, 0x02, 0x03)
    target_cmd = "BEGIN BLOCK (0x01, 0x02, 0x03)"
    build_32bit_frame_and_test(test_data, "", target_cmd)
    test_data = build_firmware_frame(0xBD, 0x01, 0x02, 0x03)
    target_cmd = "TRANSFER BLOCK DATA (0x01, 0x02, 0x03)"
    build_32bit_frame_and_test(test_data, "", target_cmd)


# refer to iec62386 105 2020 Table 1
#          iec62386 105 2020 Table 6
@pytest.mark.parametrize(
    "target_cmd,opcode_byte_2",
    [
        ("START FW TRANSFER", 0x00),
        ("RESTART FW", 0x01),
        ("ENABLE RESTART", 0x02),
        ("FINISH FW UPDATE", 0x03),
        ("CANCEL FW UPDATE", 0x04),
        ("QUERY FW UPDATE FEATURES", 0x05),
        ("QUERY FW RESTART ENABLED", 0x06),
        ("QUERY FW UPDATE RUNNING", 0x07),
        ("QUERY BLOCK FAULT", 0x08),
    ],
)
def test_firmware_update_standard_command(target_cmd, opcode_byte_2):
    opcode_byte_1 = 0xFB
    opcode_byte_3 = 0x00
    # broadcast
    test_data = build_firmware_frame(0xFE, opcode_byte_1, opcode_byte_2, opcode_byte_3)
    target_adr = "BC GEAR"
    build_32bit_frame_and_test(test_data, target_adr, target_cmd)
    test_data = build_firmware_frame(0xFF, opcode_byte_1, opcode_byte_2, opcode_byte_3)
    target_adr = "BC DEV"
    build_32bit_frame_and_test(test_data, target_adr, target_cmd)
    # broadcast unadressed
    test_data = build_firmware_frame(0xFC, opcode_byte_1, opcode_byte_2, opcode_byte_3)
    target_adr = "BC GEAR UN"
    build_32bit_frame_and_test(test_data, target_adr, target_cmd)
    test_data = build_firmware_frame(0xFD, opcode_byte_1, opcode_byte_2, opcode_byte_3)
    target_adr = "BC DEV UN"
    build_32bit_frame_and_test(test_data, target_adr, target_cmd)
    # short address
    for short_address in range(0x40):
        test_data = build_firmware_frame(
            (short_address << 1), opcode_byte_1, opcode_byte_2, opcode_byte_3
        )
        target_adr = f"G{short_address:02}"
        build_32bit_frame_and_test(test_data, target_adr, target_cmd)
        test_data = build_firmware_frame(
            (short_address << 1) + 1, opcode_byte_1, opcode_byte_2, opcode_byte_3
        )
        target_adr = f"D{short_address:02}"
        build_32bit_frame_and_test(test_data, target_adr, target_cmd)
