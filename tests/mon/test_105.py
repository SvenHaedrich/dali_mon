import pytest
import os
import sys

# locate the DALI module
here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, "../../source"))
import DALI

ADDRESS_WIDTH = 12


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
    frame = DALI.Raw_Frame(
        length=32,
        data=(
            0xFE000000 + (opcode_byte_1 << 16) + (opcode_byte_2 << 8) + opcode_byte_3
        ),
    )
    decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
    target_command = "BC GEAR".ljust(ADDRESS_WIDTH) + name
    assert decoded_command.cmd() == target_command
    frame = DALI.Raw_Frame(
        length=32,
        data=(
            0xFF000000 + (opcode_byte_1 << 16) + (opcode_byte_2 << 8) + opcode_byte_3
        ),
    )
    decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
    target_command = "BC DEV".ljust(ADDRESS_WIDTH) + name
    assert decoded_command.cmd() == target_command
    # broadcast unadressed
    frame = DALI.Raw_Frame(
        length=32,
        data=(
            0xFC000000 + (opcode_byte_1 << 16) + (opcode_byte_2 << 8) + opcode_byte_3
        ),
    )
    decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
    target_command = "BC GEAR UN".ljust(ADDRESS_WIDTH) + name
    assert decoded_command.cmd() == target_command
    frame = DALI.Raw_Frame(
        length=32,
        data=(
            0xFD000000 + (opcode_byte_1 << 16) + (opcode_byte_2 << 8) + opcode_byte_3
        ),
    )
    decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
    target_command = "BC DEV UN".ljust(ADDRESS_WIDTH) + name
    assert decoded_command.cmd() == target_command
    # short address
    for short_address in range(0x40):
        frame = DALI.Raw_Frame(
            length=32,
            data=(
                ((short_address << 1) << 24)
                + (opcode_byte_1 << 16)
                + (opcode_byte_2 << 8)
                + opcode_byte_3
            ),
        )
        decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
        target_command = f"G{short_address:02}".ljust(ADDRESS_WIDTH) + name
        assert decoded_command.cmd() == target_command
        frame = DALI.Raw_Frame(
            length=32,
            data=(
                (((short_address << 1) + 1) << 24)
                + (opcode_byte_1 << 16)
                + (opcode_byte_2 << 8)
                + opcode_byte_3
            ),
        )
        decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
        target_command = f"D{short_address:02}".ljust(ADDRESS_WIDTH) + name
        assert decoded_command.cmd() == target_command
