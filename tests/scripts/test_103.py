import pytest
import os
import sys
# locate the DALI module
here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, '../../source'))

import DALI


# refer to iec62386 103 Table 21
@pytest.mark.parametrize("name,opcode",
    [("IDENTIFY DEVICE", 0x00),
     ("RESET POWER CYCLE SEEN", 0x01),
     ("RESET", 0x10),
     ("RESET MEMORY BANK (DTR0)", 0x11),
     ("SET SHORT ADDRESS (DTR0)", 0x14),
     ("ENABLE WRITE MEMORY", 0x15),
     ("ENABLE APPLICATION CONTROLLER", 0x16),
     ("DISABLE APPLICATION CONTROLLER", 0x17)
    ]
)
def test_device_standard_command(name,opcode):
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
    for short_address in range (0,0x40):
        frame.data = 0x01FE00 + (short_address <<17) + opcode
        decoded_command = DALI.Decode(frame, DALI.DeviceType.LED)
        target_command = F"A{short_address:02}".ljust(10) + name
        assert decoded_command.cmd() == target_command
    # group address
    for group_address in range (0,0x10):
        frame.data = 0x81FE00 + (group_address << 17) + opcode
        decoded_command = DALI.Decode(frame, DALI.DeviceType.LED)
        target_command = F"G{group_address:02}".ljust(10) + name
        assert decoded_command.cmd() == target_command


@pytest.mark.parametrize("opcode",[0x02,0x03,0x04])
def test_device_undefined_codes(opcode):
    frame = DALI.Raw_Frame()
    frame.length = 24
    # broadcast
    frame.data = 0xFFFE00 + opcode
    decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
    target_command = "BC".ljust(10) + "---"
    assert decoded_command.cmd()[:len(target_command)] == target_command
    # broadcast unadressed
    frame.data = 0xFDFE00 + opcode
    decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
    target_command = "BC unadr.".ljust(10) + "---"
    assert decoded_command.cmd()[:len(target_command)] == target_command
    # short address
    for short_address in range (0,0x40):
        frame.data = 0x01FE00 + (short_address <<17) + opcode
        decoded_command = DALI.Decode(frame, DALI.DeviceType.LED)
        target_command = F"A{short_address:02}".ljust(10) + "---"
        assert decoded_command.cmd()[:len(target_command)] == target_command
    # group address
    for group_address in range (0,0x10):
        frame.data = 0x81FE00 + (group_address << 17) + opcode
        decoded_command = DALI.Decode(frame, DALI.DeviceType.LED)
        target_command = F"G{group_address:02}".ljust(10) + "---"
        assert decoded_command.cmd()[:len(target_command)] == target_command

def test_power_cycle_event():
    frame = DALI.Raw_Frame()
    frame.length = 24
    # undefined device
    frame.data = 0xFEE000
    decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
    target_command = " ".ljust(10) + "POWER CYCLE EVENT"
    assert decoded_command.cmd() == target_command
    # device with short address
    for short_address in range (0,0x40):
        frame.data = 0xFEE000 + (1<<6) + short_address
        decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
        target_command = F"A{short_address:02X}".ljust(10) + "POWER CYCLE EVENT"
        assert decoded_command.cmd() == target_command
    # device is group member
    for group_address in range(0,0x10):
        frame.data = 0xFEE000 + (1<<12) + (group_address<<7)
        decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
        target_command = F"G{group_address:02X}".ljust(10) + "POWER CYCLE EVENT"
        assert decoded_command.cmd() == target_command
    # device with group and short address
    for group_address in range(0,0x10):
        frame.data = 0xFEE000 + (1<<12) + (group_address<<7) + (1<<6) + (group_address+1)
        decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
        target_command = F"G{group_address:02X} A{(group_address+1):02X}".ljust(10) + "POWER CYCLE EVENT"
        assert decoded_command.cmd() == target_command
