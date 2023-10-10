import pytest

from DALI.dali_interface.source.frame import DaliFrame
from DALI.forward_frame_24bit import ForwardFrame24Bit
from DALI.decode import Decode


def build_24bit_frame_and_test(
    test_data: int, target_adr: str, target_cmd: str
) -> None:
    test_frame = DaliFrame(length=ForwardFrame24Bit.LENGTH, data=test_data)
    target_data = f"{test_data:06X}"
    data_str, adr, cmd = Decode(test_frame).get_strings()
    assert data_str == target_data
    assert adr == target_adr
    assert cmd[: len(target_cmd)] == target_cmd


# refer to iec62386 103 Table 21
@pytest.mark.parametrize(
    "target_cmd,opcode",
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
        ("REMOVE FROM DEVICE GROUPS 0-15 (DTR2:DTR1)", 0x1B),
        ("REMOVE FROM DEVICE GROUPS 16-31 (DTR2:DTR1)", 0x1C),
        ("START QUIESCENT MODE", 0x1D),
        ("STOP QUIESCENT MODE", 0x1E),
        ("ENABLE POWER CYCLE NOTIFICATION", 0x1F),
        ("DISABLE POWER CYCLE NOTIFICATION", 0x20),
        ("QUERY DEVICE STATUS", 0x30),
        ("QUERY APPLICATION CONTROLLER ERROR", 0x31),
        ("QUERY INPUT DEVICE ERROR", 0x32),
        ("QUERY MISSING SHORT ADDRESS", 0x33),
        ("QUERY VERSION NUMBER", 0x34),
        ("QUERY NUMBER OF INSTANCES", 0x35),
        ("QUERY CONTENT DTR0", 0x36),
        ("QUERY CONTENT DTR1", 0x37),
        ("QUERY CONTENT DTR2", 0x38),
        ("QUERY RANDOM ADDRESS (H)", 0x39),
        ("QUERY RANDOM ADDRESS (M)", 0x3A),
        ("QUERY RANDOM ADDRESS (L)", 0x3B),
        ("READ MEMORY LOCATION (DTR1,DTR0)", 0x3C),
        ("QUERY APPLICATION CONTROLLER ENABLED", 0x3D),
        ("QUERY OPERATING MODE", 0x3E),
        ("QUERY MANUFACTURER SPECIFIC MODE", 0x3F),
        ("QUERY QUIESCENT MODE", 0x40),
        ("QUERY DEVICE GROUPS 0-7", 0x41),
        ("QUERY DEVICE GROUPS 8-15", 0x42),
        ("QUERY DEVICE GROUPS 16-23", 0x43),
        ("QUERY DEVICE GROUPS 24-31", 0x44),
        ("QUERY POWER CYCLE NOTIFICATION", 0x45),
        ("QUERY DEVICE CAPABILITIES", 0x46),
        ("QUERY EXTENDED VERSION NUMBER (DTR0)", 0x47),
        ("QUERY RESET STATE", 0x48),
        ("QUERY APPLICATION CONTROLLER ALWAYS ACTIVE", 0x49),
    ],
)
def test_device_standard_command(target_cmd, opcode):
    # broadcast
    build_24bit_frame_and_test((0xFFFE00 + opcode), "BC DEV", target_cmd)
    # broadcast unadressed
    build_24bit_frame_and_test((0xFDFE00 + opcode), "BC DEV UN", target_cmd)
    # short address
    for short_address in range(0x40):
        target_adr = f"D{short_address:02}"
        test_data = 0x01FE00 + (short_address << 17) + opcode
        build_24bit_frame_and_test(test_data, target_adr, target_cmd)
    # group address
    for group_address in range(0x10):
        target_adr = f"DG{group_address:02}"
        test_data = 0x81FE00 + (group_address << 17) + opcode
        build_24bit_frame_and_test(test_data, target_adr, target_cmd)


@pytest.mark.parametrize(
    "target_cmd,instance_byte",
    [
        ("TERMINATE", 0x00),
        ("RANDOMISE", 0x02),
        ("COMPARE", 0x03),
        ("WITHDRAW", 0x04),
        ("QUERY SHORT ADDRESS", 0x0A),
    ],
)
def test_simple_special_commands(target_cmd, instance_byte):
    test_data = (0xC1 << 16) + (instance_byte << 8)
    build_24bit_frame_and_test(test_data, "", target_cmd)


@pytest.mark.parametrize("opcode", [0x02, 0x03, 0x04])
def test_device_undefined_codes(opcode):
    # broadcast
    test_data = 0xFFFE00 + opcode
    build_24bit_frame_and_test(test_data, "BC DEV", "---")
    # broadcast unadressed
    test_data = 0xFDFE00 + opcode
    build_24bit_frame_and_test(test_data, "BC DEV UN", "---")
    # short address
    for short_address in range(0x40):
        target_adr = f"D{short_address:02}"
        test_data = 0x01FE00 + (short_address << 17) + opcode
        build_24bit_frame_and_test(test_data, target_adr, "---")
    # group address
    for group_address in range(0x10):
        target_adr = f"DG{group_address:02}"
        test_data = 0x81FE00 + (group_address << 17) + opcode
        build_24bit_frame_and_test(test_data, target_adr, "---")


def test_power_cycle_event():
    # see IEC62386-103:2022 9.7.2 Table 7 - Device address information in power cycle event
    # undefined device
    test_data = 0xFEE000
    target_adr = ""
    target_cmd = "POWER CYCLE EVENT"
    build_24bit_frame_and_test(test_data, target_adr, target_cmd)
    # device with short address
    for short_address in range(0x40):
        test_data = 0xFEE000 + (1 << 6) + short_address
        target_adr = f"D{short_address:02}"
        build_24bit_frame_and_test(test_data, target_adr, target_cmd)
    # device is group member
    for group_address in range(0x10):
        test_data = 0xFEE000 + (1 << 12) + (group_address << 7)
        target_adr = f"DG{group_address:02}"
        build_24bit_frame_and_test(test_data, target_adr, target_cmd)
    # device with group and short address
    for group_address in range(0x10):
        for short_address in range(0x40):
            test_data = (
                0xFEE000 + (1 << 12) + (group_address << 7) + (1 << 6) + short_address
            )
            target_adr = f"DG{group_address:02} D{short_address:02}"
            build_24bit_frame_and_test(test_data, target_adr, target_cmd)


def test_event_scheme_decoding():
    # see IEC62386-103-2022 7.2.2.1 Table 3
    # eventScheme Device (0)
    target_cmd = "EVENT DATA 0x000 = 0 = 000000000000b"
    for short_address in range(0x40):
        for instance_type in range(0x20):
            test_data = (short_address << 17) + (instance_type << 10)
            target_adr = f"D{short_address:02},T{instance_type:02}"
            build_24bit_frame_and_test(test_data, target_adr, target_cmd)
    # eventScheme Device and Instance (2)
    for short_address in range(0x40):
        for instance_number in range(0x20):
            test_data = (short_address << 17) + (1 << 15) + (instance_number << 10)
            target_adr = f"D{short_address:02},I{instance_number:02}"
            build_24bit_frame_and_test(test_data, target_adr, target_cmd)
    # eventScheme Device group (3)
    for device_group in range(0x20):
        for instance_type in range(0x20):
            test_data = (1 << 23) + (device_group << 17) + (instance_type << 10)
            target_adr = f"DG{device_group:02},T{instance_type:02}"
            build_24bit_frame_and_test(test_data, target_adr, target_cmd)
    # eventScheme Instance (0)
    for instance_type in range(0x20):
        for instance_number in range(0x20):
            test_data = (
                (1 << 23) + (instance_type << 17) + (1 << 15) + (instance_number << 10)
            )
            target_adr = f"T{instance_type:02},I{instance_number:02}"
            build_24bit_frame_and_test(test_data, target_adr, target_cmd)
    # eventScheme Instance (0)
    for instance_groups in range(0x20):
        for instance_types in range(0x20):
            test_data = (3 << 22) + (instance_groups << 17) + (instance_types << 10)
            target_adr = f"IG{instance_groups:02},T{instance_types:02}"
            build_24bit_frame_and_test(test_data, target_adr, target_cmd)


def test_reserved_event_schemes():
    # see IEC62386-103-2022 7.2.2.1 Table 3
    target_adr = ""
    target_cmd = "RESERVED EVENT"
    for upper_bits in range(0x10):
        for lower_bits in range(0x20):
            test_data = (3 << 22) + (upper_bits << 17) + (1 << 15) + (lower_bits << 10)
            build_24bit_frame_and_test(test_data, target_adr, target_cmd)
    for upper_bits in range(0x8):
        for lower_bits in range(0x20):
            test_data = (7 << 21) + (upper_bits << 17) + (1 << 15) + (lower_bits << 10)
            build_24bit_frame_and_test(test_data, target_adr, target_cmd)
    for upper_bits in range(0x4):
        for lower_bits in range(0x20):
            test_data = (
                (0xF << 20) + (upper_bits << 17) + (1 << 15) + (lower_bits << 10)
            )
            build_24bit_frame_and_test(test_data, target_adr, target_cmd)
    for upper_bits in range(0x2):
        for lower_bits in range(0x20):
            test_data = (
                (0x1F << 19) + (upper_bits << 17) + (1 << 15) + (lower_bits << 10)
            )
            build_24bit_frame_and_test(test_data, target_adr, target_cmd)


def run_thru_instance_addressing(basic_data, basic_addressing, target_cmd):
    for instance_number in range(0x20):
        target_adr = basic_addressing + f",I{instance_number:02}"
        test_data = basic_data + (instance_number << 8)
        build_24bit_frame_and_test(test_data, target_adr, target_cmd)
    for instance_group in range(0x20):
        target_adr = basic_addressing + f",IG{instance_group:02}"
        test_data = basic_data + (instance_group << 8) + (1 << 15)
        build_24bit_frame_and_test(test_data, target_adr, target_cmd)
    for instance_typ in range(0x20):
        target_adr = basic_addressing + f",T{instance_typ:02}"
        test_data = basic_data + (instance_typ << 8) + (3 << 14)
        build_24bit_frame_and_test(test_data, target_adr, target_cmd)
    for instance_number in range(0x20):
        target_adr = basic_addressing + f",FI{instance_number:02}"
        test_data = basic_data + (instance_number << 8) + (1 << 13)
        build_24bit_frame_and_test(test_data, target_adr, target_cmd)
    for instance_group in range(0x20):
        target_adr = basic_addressing + f",FG{instance_group:02}"
        test_data = basic_data + (instance_group << 8) + (5 << 13)
        build_24bit_frame_and_test(test_data, target_adr, target_cmd)
    for instance_typ in range(0x20):
        target_adr = basic_addressing + f",FT{instance_typ:02}"
        test_data = basic_data + (instance_typ << 8) + (3 << 13)
        build_24bit_frame_and_test(test_data, target_adr, target_cmd)


# TODO add tests for broadcast


@pytest.mark.parametrize(
    "command_name,opcode_byte",
    [
        ("ENABLE INSTANCE", 0x62),
        ("DISABLE INSTANCE", 0x63),
        ("SET PRIMARY INSTANCE GROUP (DTR0)", 0x64),
        ("SET INSTANCE GROUP 1 (DTR0)", 0x65),
        ("SET INSTANCE GROUP 2 (DTR0)", 0x66),
        ("SET EVENT SCHEME (DTR0)", 0x67),
        ("SET EVENT FILTER (DTR2,DTR1,DTR0)", 0x68),
        ("SET INSTANCE TYPE (DTR0)", 0x69),
        ("SET INSTANCE CONFIGURATION (DTR0,DTR2:DTR1)", 0x6A),
        ("QUERY INSTANCE TYPE", 0x80),
        ("QUERY RESOLUTION", 0x81),
        ("QUERY INSTANCE ERROR", 0x82),
        ("QUERY INSTANCE STATUS", 0x83),
        ("QUERY EVENT PRIORITY", 0x84),
        ("QUERY INSTANCE ENABLED", 0x86),
    ],
)
def test_instance_command(command_name, opcode_byte):
    for short_address in range(0x40):
        basic_data = (short_address << 17) + (1 << 16) + opcode_byte
        run_thru_instance_addressing(basic_data, f"D{short_address:02}", command_name)


def test_initialise_short_address():
    for short_address in range(0x40):
        test_data = 0xC10100 + short_address
        target_cmd = f"INITIALISE (D{short_address:02})"
        build_24bit_frame_and_test(test_data, "", target_cmd)


@pytest.mark.parametrize(
    "test_data,target_cmd",
    [
        (0xC1017F, "INITIALISE (UNADDRESSED)"),
        (0xC101FF, "INITIALISE (ALL)"),
        (0xC10150, "INITIALISE (NONE) - 0x50"),
    ],
)
def test_initialise_special_cases(test_data, target_cmd):
    build_24bit_frame_and_test(test_data, "", target_cmd)
