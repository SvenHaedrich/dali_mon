import pytest
import os
import sys

# locate the DALI module
here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, "../../source"))

import DALI


# refer to iec62386 103 Table 21
@pytest.mark.parametrize(
    "name,opcode",
    [
        ("IDENTIFY DEVICE", 0x00),
        ("RESET POWER CYCLE SEEN", 0x01),
        ("RESET", 0x10),
        ("RESET MEMORY BANK (DTR0)", 0x11),
        ("SET SHORT ADDRESS (DTR0)", 0x14),
        ("ENABLE WRITE MEMORY", 0x15),
        ("ENABLE APPLICATION CONTROLLER", 0x16),
        ("DISABLE APPLICATION CONTROLLER", 0x17),
        ("SET OPERATING MODE (DTR0)", 0x18),
        ("ADD TO DEVICE GROUPS 0-15 (DTR2:DTR1)", 0x19),
        ("ADD TO DEVICE GROUPS 16-31 (DTR2:DTR1)", 0x1A),
    ],
)
def test_device_standard_command(name, opcode):
    frame = DALI.Raw_Frame()
    frame.length = 24
    # broadcast
    frame.data = 0xFFFE00 + opcode
    decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
    target_command = "BC".ljust(10) + name
    assert decoded_command.cmd() == target_command
    # broadcast unadressed
    frame.data = 0xFDFE00 + opcode
    decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
    target_command = "BC unadr.".ljust(10) + name
    assert decoded_command.cmd() == target_command
    # short address
    for short_address in range(0, 0x40):
        frame.data = 0x01FE00 + (short_address << 17) + opcode
        decoded_command = DALI.Decode(frame, DALI.DeviceType.LED)
        target_command = f"A{short_address:02}".ljust(10) + name
        assert decoded_command.cmd() == target_command
    # group address
    for group_address in range(0, 0x10):
        frame.data = 0x81FE00 + (group_address << 17) + opcode
        decoded_command = DALI.Decode(frame, DALI.DeviceType.LED)
        target_command = f"G{group_address:02}".ljust(10) + name
        assert decoded_command.cmd() == target_command


@pytest.mark.parametrize("opcode", [0x02, 0x03, 0x04])
def test_device_undefined_codes(opcode):
    frame = DALI.Raw_Frame()
    frame.length = 24
    # broadcast
    frame.data = 0xFFFE00 + opcode
    decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
    target_command = "BC".ljust(10) + "---"
    assert decoded_command.cmd()[: len(target_command)] == target_command
    # broadcast unadressed
    frame.data = 0xFDFE00 + opcode
    decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
    target_command = "BC unadr.".ljust(10) + "---"
    assert decoded_command.cmd()[: len(target_command)] == target_command
    # short address
    for short_address in range(0, 0x40):
        frame.data = 0x01FE00 + (short_address << 17) + opcode
        decoded_command = DALI.Decode(frame, DALI.DeviceType.LED)
        target_command = f"A{short_address:02}".ljust(10) + "---"
        assert decoded_command.cmd()[: len(target_command)] == target_command
    # group address
    for group_address in range(0, 0x10):
        frame.data = 0x81FE00 + (group_address << 17) + opcode
        decoded_command = DALI.Decode(frame, DALI.DeviceType.LED)
        target_command = f"G{group_address:02}".ljust(10) + "---"
        assert decoded_command.cmd()[: len(target_command)] == target_command


def test_power_cycle_event():
    frame = DALI.Raw_Frame()
    frame.length = 24
    # undefined device
    frame.data = 0xFEE000
    decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
    target_command = " ".ljust(10) + "POWER CYCLE EVENT"
    assert decoded_command.cmd() == target_command
    # device with short address
    for short_address in range(0, 0x40):
        frame.data = 0xFEE000 + (1 << 6) + short_address
        decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
        target_command = f"A{short_address:02}".ljust(10) + "POWER CYCLE EVENT"
        assert decoded_command.cmd() == target_command
    # device is group member
    for group_address in range(0, 0x10):
        frame.data = 0xFEE000 + (1 << 12) + (group_address << 7)
        decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
        target_command = f"G{group_address:02}".ljust(10) + "POWER CYCLE EVENT"
        assert decoded_command.cmd() == target_command
    # device with group and short address
    for group_address in range(0, 0x10):
        frame.data = (
            0xFEE000 + (1 << 12) + (group_address << 7) + (1 << 6) + (group_address + 1)
        )
        decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
        target_command = (
            f"G{group_address:02} A{(group_address+1):02}".ljust(10)
            + "POWER CYCLE EVENT"
        )
        assert decoded_command.cmd() == target_command


def test_event_scheme_decoding():
    # see IEC62386-103-2022 7.2.2.1 Table 3
    frame = DALI.Raw_Frame()
    frame.length = 24
    # eventScheme Device (0)
    for short_address in range(0, 0x40):
        for instance_type in range(0, 0x20):
            frame.data = (short_address << 17) + (instance_type << 10)
            decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
            target_command = (
                f"A{short_address:02},T{instance_type:02}".ljust(10)
                + "EVENT DATA 0x000 = 0 = 000000000000b"
            )
            assert decoded_command.cmd() == target_command
    # eventScheme Device and Instance (2)
    for short_address in range(0, 0x40):
        for instance_number in range(0, 0x20):
            frame.data = (short_address << 17) + (1 << 15) + (instance_number << 10)
            decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
            target_command = (
                f"A{short_address:02},I{instance_number:02}".ljust(10)
                + "EVENT DATA 0x000 = 0 = 000000000000b"
            )
            assert decoded_command.cmd() == target_command
    # eventScheme Device group (3)
    for device_group in range(0, 0x20):
        for instance_type in range(0, 0x20):
            frame.data = (1 << 23) + (device_group << 17) + (instance_type << 10)
            decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
            target_command = (
                f"G{device_group:02},T{instance_type:02}".ljust(10)
                + "EVENT DATA 0x000 = 0 = 000000000000b"
            )
            assert decoded_command.cmd() == target_command
    # eventScheme Instance (0)
    for instance_type in range(0, 0x20):
        for instance_number in range(0, 0x20):
            frame.data = (
                (1 << 23) + (instance_type << 17) + (1 << 15) + (instance_number << 10)
            )
            decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
            target_command = (
                f"T{instance_type:02},I{instance_number:02}".ljust(10)
                + "EVENT DATA 0x000 = 0 = 000000000000b"
            )
            assert decoded_command.cmd() == target_command
    # eventScheme Instance (0)
    for instance_groups in range(0, 0x20):
        for instance_types in range(0, 0x20):
            frame.data = (3 << 22) + (instance_groups << 17) + (instance_types << 10)
            decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
            target_command = (
                f"IG{instance_groups:02},T{instance_types:02}".ljust(10)
                + "EVENT DATA 0x000 = 0 = 000000000000b"
            )
            assert decoded_command.cmd() == target_command


def test_reserved_event_schemes():
    # see IEC62386-103-2022 7.2.2.1 Table 3
    frame = DALI.Raw_Frame()
    frame.length = 24
    target_command = "".ljust(10) + "RESERVED EVENT"
    for upper_bits in range(0, 0x10):
        for lower_bits in range(0, 0x20):
            frame.data = (3 << 22) + (upper_bits << 17) + (1 << 15) + (lower_bits << 10)
            decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
            assert decoded_command.cmd() == target_command
    for upper_bits in range(0, 0x8):
        for lower_bits in range(0, 0x20):
            frame.data = (7 << 21) + (upper_bits << 17) + (1 << 15) + (lower_bits << 10)
            decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
            assert decoded_command.cmd() == target_command
    for upper_bits in range(0, 0x4):
        for lower_bits in range(0, 0x20):
            frame.data = (
                (0xF << 20) + (upper_bits << 17) + (1 << 15) + (lower_bits << 10)
            )
            decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
            assert decoded_command.cmd() == target_command
    for upper_bits in range(0, 0x2):
        for lower_bits in range(0, 0x20):
            frame.data = (
                (0x1F << 19) + (upper_bits << 17) + (1 << 15) + (lower_bits << 10)
            )
            decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
            assert decoded_command.cmd() == target_command
