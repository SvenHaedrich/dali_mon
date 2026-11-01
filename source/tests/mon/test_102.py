import pytest
from dali_interface import DaliFrame

from DALI.backframe_8bit import Backframe8Bit
from DALI.decode import Decode, DeviceType
from DALI.forward_frame_16bit import ForwardFrame16Bit


def build_16bit_frame_and_test(
    test_data: int, target_adr: str, target_cmd: str
) -> None:
    test_frame = DaliFrame(length=ForwardFrame16Bit.LENGTH, data=test_data)
    target_data = f"{test_data:04X}"
    data_str, adr, cmd = Decode(test_frame).get_strings()
    assert data_str == target_data
    assert adr == target_adr
    assert cmd[: len(target_cmd)] == target_cmd


def test_backframe():
    for data in range(0x100):
        test_frame = DaliFrame(length=Backframe8Bit.LENGTH, data=data)
        decoder = Decode(test_frame)
        data_str, address, command = decoder.get_strings()
        target_command = f"DATA 0x{data:02X}"
        assert data_str == f"{data:02X}"
        assert address == ""
        assert command[: len(target_command)] == target_command


def test_broadcast_dapc():
    # refer to iec62386 102 7.2.1
    target_adr = "BC GEAR"
    for level in range(0x100):
        test_data = 0xFE00 + level
        target_cmd = f"DAPC {level}"
        build_16bit_frame_and_test(test_data, target_adr, target_cmd)


def test_short_address_dapc():
    # refer to iec62386 102 7.2.1
    for short_address in range(0x40):
        target_adr = f"G{short_address:02}"
        for level in range(0x100):
            test_data = (short_address << 9) + level
            target_cmd = f"DAPC {level}"
            build_16bit_frame_and_test(test_data, target_adr, target_cmd)


def test_group_address_dapc():
    # refer to iec62386 102 7.2.1
    for group_address in range(0x10):
        target_adr = f"GG{group_address:02}"
        for level in range(0x100):
            test_data = 0x8000 + (group_address << 9) + level
            target_cmd = f"DAPC {level}"
            build_16bit_frame_and_test(test_data, target_adr, target_cmd)


def test_reserved():
    # refer to iec62386 102 7.2.1
    target_cmd = "RESERVED"
    target_adr = ""
    for code in range(0xCC00, 0xFC00):
        build_16bit_frame_and_test(code, target_adr, target_cmd)


# refer to iec62386 102 Table 15
@pytest.mark.parametrize(
    "target_cmd,opcode",
    [
        ("OFF", 0x00),
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
        ("CONTINUOUS UP", 0x0B),
        ("CONTINUOUS DOWN", 0x0C),
        ("RESET", 0x20),
        ("STORE ACTUAL LEVEL IN DTR0", 0x21),
        ("SAVE PERSISTENT VARIABLES (DEPRECATED)", 0x22),
        ("SET OPERATING MODE (DTR0)", 0x23),
        ("RESET MEMORY BANK (DTR0)", 0x24),
        ("IDENTIFY DEVICE", 0x25),
        ("SET MAX LEVEL (DTR0)", 0x2A),
        ("SET MIN LEVEL (DTR0)", 0x2B),
        ("SET SYSTEM FAILURE LEVEL (DTR0)", 0x2C),
        ("SET POWER ON LEVEL (DTR0)", 0x2D),
        ("SET FADE TIME (DTR0)", 0x2E),
        ("SET FADE RATE (DTR0)", 0x2F),
        ("SET EXTENDED FADE TIME (DTR0)", 0x30),
    ],
)
def test_command(target_cmd, opcode):
    # broadcast
    target_adr = "BC GEAR"
    test_data = 0xFF00 + opcode
    build_16bit_frame_and_test(test_data, target_adr, target_cmd)
    # broadcast unadressed
    target_adr = "BC GEAR UN"
    test_data = 0xFD00 + opcode
    build_16bit_frame_and_test(test_data, target_adr, target_cmd)
    # short address
    for short_address in range(0x40):
        target_adr = f"G{short_address:02}"
        test_data = 0x0100 + (short_address << 9) + opcode
        build_16bit_frame_and_test(test_data, target_adr, target_cmd)
    # group address
    for group_address in range(0x10):
        target_adr = f"GG{group_address:02}"
        test_data = 0x8100 + (group_address << 9) + opcode


@pytest.mark.parametrize(
    "name,opcode",
    [
        ("GO TO SCENE", 0x10),
        ("SET SCENE (DTR0)", 0x40),
        ("REMOVE FROM SCENE", 0x50),
        ("ADD TO GROUP", 0x60),
        ("REMOVE FROM GROUP", 0x70),
        ("QUERY SCENE LEVEL", 0xB0),
    ],
)
def test_count_command(name, opcode):
    for counter in range(0x10):
        scene_opcode = opcode + counter
        scene_name = name + f" {counter}"
        test_command(scene_name, scene_opcode)


@pytest.mark.parametrize(
    "opcode",
    [
        0x0D,
        0x0E,
        0x0F,
        0x26,
        0x27,
        0x28,
        0x29,
        0x31,
        0x32,
        0x33,
        0x34,
        0x35,
        0x36,
        0x37,
        0x38,
        0x39,
        0x3A,
        0x3B,
        0x3C,
        0x3D,
        0x3E,
        0x3F,
        0x82,
        0x83,
        0x84,
        0x85,
        0x86,
        0x87,
        0x88,
        0x89,
        0x8A,
        0x8B,
        0x8C,
        0x8D,
        0x8E,
        0x8F,
        0xAB,
        0xAC,
        0xAD,
        0xAE,
        0xAF,
        0xC6,
        0xC7,
        0xC8,
        0xC9,
        0xCA,
        0xCB,
    ],
)
def test_undefined_codes(opcode):
    test_command("---", opcode)


@pytest.mark.parametrize(
    "target_cmd,address_byte",
    [
        ("TERMINATE", 0xA1),
        ("RANDOMISE", 0xA7),
        ("COMPARE", 0xA9),
        ("WITHDRAW", 0xAB),
        ("PING", 0xAD),
        ("QUERY SHORT ADDRESS", 0xBB),
    ],
)
def test_simple_special_command(target_cmd, address_byte):
    # valid opcode byte
    target_adr = ""
    test_data = address_byte << 8
    build_16bit_frame_and_test(test_data, target_adr, target_cmd)
    # invalid opcode byte
    target_cmd = "---"
    for opcode_byte in range(1, 0x100):
        test_data = (address_byte << 8) + opcode_byte
        build_16bit_frame_and_test(test_data, target_adr, target_cmd)


def test_initialise_short_address():
    target_adr = ""
    for short_address in range(0x40):
        test_data = 0xA500 + (short_address << 1) + 1
        target_cmd = f"INITIALISE (G{short_address:02})"
        build_16bit_frame_and_test(test_data, target_adr, target_cmd)


@pytest.mark.parametrize(
    "test_data,target_cmd",
    [
        (0xA5FF, "INITIALISE (UNADDRESSED)"),
        (0xA500, "INITIALISE (ALL)"),
        (0xA550, "INITIALISE (NONE) - 0x50"),
    ],
)
def test_initialise_special_cases(test_data, target_cmd):
    target_adr = ""
    build_16bit_frame_and_test(test_data, target_adr, target_cmd)


# refer to iec62386 102 11.2: ENABLE DEVICE TYPE selects the meaning of
# the application extended commands 0xE0 to 0xFF only, the standard
# commands 0x00 to 0xDF keep their meaning
@pytest.mark.parametrize(
    "device_type", [DeviceType.LED, DeviceType.SWITCH, DeviceType.COLOUR]
)
def test_standard_command_after_enable_device_type(device_type):
    enable_frame = DaliFrame(length=ForwardFrame16Bit.LENGTH, data=0xC100 + device_type)
    active_device_type = Decode(enable_frame).get_next_device_type()
    assert active_device_type == device_type
    for opcode in range(0xE0):
        test_frame = DaliFrame(length=ForwardFrame16Bit.LENGTH, data=0xFF00 + opcode)
        _, _, target_cmd = Decode(test_frame).get_strings()
        _, adr, cmd = Decode(test_frame, active_device_type).get_strings()
        assert adr == "BC GEAR"
        assert cmd == target_cmd, f"opcode 0x{opcode:02X}"


def decode_sequence(frames: list[DaliFrame]) -> str:
    # pass the device type from frame to frame like dali_mon does,
    # return the command of the last frame
    device_type = DeviceType.NONE
    for frame in frames:
        decoding = Decode(frame, device_type)
        device_type = decoding.get_next_device_type()
    return decoding.get_strings()[2]


# refer to iec62386 102 11.2: ENABLE DEVICE TYPE stays active until the
# next command accepted by control gear, frames that are not 102 forward
# frames don't end it
@pytest.mark.parametrize(
    "device_type,target_cmd",
    [
        (DeviceType.LED, "REFERENCE SYSTEM POWER"),
        (DeviceType.SWITCH, "REFERENCE SYSTEM POWER"),
        (DeviceType.COLOUR, "SET TEMPORARY X-COORDINATE"),
    ],
)
@pytest.mark.parametrize(
    "length,data",
    [
        pytest.param(8, 0x12, id="backward frame"),
        pytest.param(24, 0xFFFE00, id="103 command"),
        pytest.param(24, 0x000000, id="103 event"),
        pytest.param(32, 0xCB000000, id="105 command"),
        pytest.param(25, 0x1FFFF00, id="eDALI frame"),
        pytest.param(17, 0x1FF90, id="Helvar frame"),
    ],
)
def test_enable_device_type_kept_by_other_frames(device_type, target_cmd, length, data):
    enable_frame = DaliFrame(length=ForwardFrame16Bit.LENGTH, data=0xC100 + device_type)
    other_frame = DaliFrame(length=length, data=data)
    command_frame = DaliFrame(length=ForwardFrame16Bit.LENGTH, data=0xFFE0)
    cmd = decode_sequence([enable_frame, other_frame, command_frame])
    assert cmd == target_cmd


@pytest.mark.parametrize(
    "device_type", [DeviceType.LED, DeviceType.SWITCH, DeviceType.COLOUR]
)
def test_enable_device_type_ended_by_gear_command(device_type):
    enable_frame = DaliFrame(length=ForwardFrame16Bit.LENGTH, data=0xC100 + device_type)
    gear_frame = DaliFrame(length=ForwardFrame16Bit.LENGTH, data=0xFF90)
    command_frame = DaliFrame(length=ForwardFrame16Bit.LENGTH, data=0xFFE0)
    cmd = decode_sequence([enable_frame, gear_frame, command_frame])
    assert cmd.startswith("--- CODE 0xE0 = 224 UNKNOWN CONTROL GEAR COMMAND")
