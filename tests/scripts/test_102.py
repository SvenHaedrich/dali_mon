import pytest
import os
import sys
# locate the DALI module
here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, '../../source'))

import DALI

def test_broadcast_dapc():
    # refer to iec62386 102 7.2.1
    frame = DALI.Raw_Frame()
    frame.length = 16
    for level in range(0,255):
        frame.data = 0xFE00 + level
        decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
        target_command = "BC".ljust(10) + F"DAPC {level}"
        assert decoded_command.cmd() == target_command


def test_short_address_dapc():
    # refer to iec62386 102 7.2.1
    frame = DALI.Raw_Frame()
    frame.length = 16
    for short_address in range (0,63):
        for level in range(0,255):
            frame.data = (short_address << 9) + level
            decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
            target_command = F"A{short_address:02}".ljust(10) + F"DAPC {level}"
            assert decoded_command.cmd() == target_command


def test_group_address_dapc():
    # refer to iec62386 102 7.2.1
    frame = DALI.Raw_Frame()
    frame.length = 16
    for group_address in range (0,15):
        for level in range(0,255):
            frame.data = 0x8000 + (group_address << 9) + level
            decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
            target_command = F"G{group_address:02}".ljust(10) + F"DAPC {level}"
            assert decoded_command.cmd() == target_command


def test_reserved():
    # refer to iec62386 102 7.2.1
    frame = DALI.Raw_Frame()
    frame.length = 16
    target_command = " "*10 + F"RESERVED"
    for frame.data in range(0xCC00, 0xFBFF):
        decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
        assert decoded_command.cmd() == target_command


# refer to iec62386 102 Table 15
@pytest.mark.parametrize("name,opcode",
    [("OFF", 0x00),
     ("UP", 0x01),
     ("DOWN", 0x02),
     ("STEP UP", 0x03),
     ("STEP DOWN", 0x04),
     ("RECALL MAX LEVEL", 0x05),
     ("RECALL MIN LEVEL", 0x06),
     ("STEP DOWN AND OFF", 0x07),
     ("ON AND STEP UP", 0x08),
     ("ENABLE DAPC SEQUENCE", 0x09),
     ("GO TO LAST ACTIVE LEVEL", 0x0A),
     ("RESET", 0x20),
     ("STORE ACTUAL LEVEL IN DTR0", 0x21),
     ("SAVE PERSISTENT VARIABLES", 0x22),
     ("SET OPERATING MODE (DTR0)", 0x23),
     ("RESET MEMORY BANK (DTR0)", 0x24),
     ("IDENTIFY DEVICE", 0x25),
     ("SET MAX LEVEL (DTR0)", 0x2A),
     ("SET MIN LEVEL (DTR0)", 0x2B),
     ("SET SYSTEM FAILURE LEVEL (DTR0)", 0x2C),
     ("SET POWER ON LEVEL (DTR0)", 0x2D),
     ("SET FADE TIME (DTR0)", 0x2E),
     ("SET FADE RATE (DTR0)", 0x2F),
     ("SET EXTENDED FADE TIME (DTR0)", 0x30)

    ]
)
def test_command(name,opcode):
    frame = DALI.Raw_Frame()
    frame.length = 16
    # broadcast
    frame.data = 0xFF00 + opcode
    decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
    target_command = "BC".ljust(10) + name
    assert decoded_command.cmd() == target_command
    # broadcast unadressed
    frame.data = 0xFD00 + opcode
    decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
    target_command = "BC unadr.".ljust(10) + name
    assert decoded_command.cmd() == target_command
    # short address
    for short_address in range (0,63):
        frame.data = 0x0100 + (short_address << 9) + opcode
        decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
        target_command = F"A{short_address:02}".ljust(10) + name
        assert decoded_command.cmd() == target_command
    # group address
    for group_address in range (0,15):
        frame.data = 0x8100 + (group_address << 9) + opcode
        decoded_command = DALI.Decode(frame, DALI.DeviceType.NONE)
        target_command = F"G{group_address:02}".ljust(10) + name
        assert decoded_command.cmd() == target_command


@pytest.mark.parametrize("name,opcode",
    [("GO TO SCENE", 0x10),
     ("SET SCENE (DTR0)", 0x40),
     ("REMOVE FROM SCENE", 0x50),
     ("ADD TO GROUP", 0x60)
    ]
)
def test_count_command(name,opcode):
    for counter in range(0,15):
        scene_opcode = opcode + counter
        scene_name = name + F" {counter}"
        test_command(scene_name, scene_opcode)