import pytest
import DALI

ADDRESS_WIDTH = 12


def build_firmware_frame(
    address_byte=0, opcode_byte_1=0, opcode_byte_2=0, opcode_byte_3=0
):
    data = address_byte & 0xFF
    data = (data << 8) + (opcode_byte_1 & 0xFF)
    data = (data << 8) + (opcode_byte_2 & 0xFF)
    data = (data << 8) + (opcode_byte_3 & 0xFF)
    return data


def test_block_commands():
    decoded_command = DALI.Decode(
        length=32, data=build_firmware_frame(0xCB, 0x01, 0x02, 0x03)
    )
    target_command = " " * ADDRESS_WIDTH + "BEGIN BLOCK (0x01, 0x02, 0x03)"
    assert decoded_command.cmd() == target_command
    decoded_command = DALI.Decode(
        length=32, data=build_firmware_frame(0xBD, 0x01, 0x02, 0x03)
    )
    target_command = " " * ADDRESS_WIDTH + "TRANSFER BLOCK DATA (0x01, 0x02, 0x03)"
    assert decoded_command.cmd() == target_command


# refer to iec62386 105 2020 Table 1
#          iec62386 105 2020 Table 6
@pytest.mark.parametrize(
    "name,opcode_byte_2",
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
def test_firmware_update_standard_command(name, opcode_byte_2):
    opcode_byte_1 = 0xFB
    opcode_byte_3 = 0x00
    # broadcast
    decoded_command = DALI.Decode(
        length=32,
        data=build_firmware_frame(0xFE, opcode_byte_1, opcode_byte_2, opcode_byte_3),
    )
    target_command = "BC GEAR".ljust(ADDRESS_WIDTH) + name
    assert decoded_command.cmd() == target_command
    decoded_command = DALI.Decode(
        length=32,
        data=build_firmware_frame(0xFF, opcode_byte_1, opcode_byte_2, opcode_byte_3),
    )
    target_command = "BC DEV".ljust(ADDRESS_WIDTH) + name
    assert decoded_command.cmd() == target_command
    # broadcast unadressed
    decoded_command = DALI.Decode(
        length=32,
        data=build_firmware_frame(0xFC, opcode_byte_1, opcode_byte_2, opcode_byte_3),
    )
    target_command = "BC GEAR UN".ljust(ADDRESS_WIDTH) + name
    assert decoded_command.cmd() == target_command
    decoded_command = DALI.Decode(
        length=32,
        data=build_firmware_frame(0xFD, opcode_byte_1, opcode_byte_2, opcode_byte_3),
    )
    target_command = "BC DEV UN".ljust(ADDRESS_WIDTH) + name
    assert decoded_command.cmd() == target_command
    # short address
    for short_address in range(0x40):
        decoded_command = DALI.Decode(
            length=32,
            data=build_firmware_frame(
                (short_address << 1), opcode_byte_1, opcode_byte_2, opcode_byte_3
            ),
        )
        target_command = f"G{short_address:02}".ljust(ADDRESS_WIDTH) + name
        assert decoded_command.cmd() == target_command
        decoded_command = DALI.Decode(
            length=32,
            data=build_firmware_frame(
                (short_address << 1) + 1, opcode_byte_1, opcode_byte_2, opcode_byte_3
            ),
        )
        target_command = f"D{short_address:02}".ljust(ADDRESS_WIDTH) + name
        assert decoded_command.cmd() == target_command
