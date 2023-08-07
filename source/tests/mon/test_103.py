import pytest
import DALI

ADDRESS_WIDTH = 14


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
def test_device_standard_command(name, opcode):
    # broadcast
    decoded_command = DALI.Decode(length=24, data=(0xFFFE00 + opcode))
    target_command = "BC DEV".ljust(ADDRESS_WIDTH) + name
    assert decoded_command.cmd() == target_command
    # broadcast unadressed
    decoded_command = DALI.Decode(length=24, data=(0xFDFE00 + opcode))
    target_command = "BC DEV UN".ljust(ADDRESS_WIDTH) + name
    assert decoded_command.cmd() == target_command
    # short address
    for short_address in range(0x40):
        decoded_command = DALI.Decode(
            length=24,
            data=(0x01FE00 + (short_address << 17) + opcode),
            device_type=DALI.DeviceType.LED,
        )
        target_command = f"D{short_address:02}".ljust(ADDRESS_WIDTH) + name
        assert decoded_command.cmd() == target_command
    # group address
    for group_address in range(0x10):
        decoded_command = DALI.Decode(
            length=24,
            data=(0x81FE00 + (group_address << 17) + opcode),
            device_type=DALI.DeviceType.LED,
        )
        target_command = f"DG{group_address:02}".ljust(ADDRESS_WIDTH) + name
        assert decoded_command.cmd() == target_command


@pytest.mark.parametrize(
    "name,instance_byte",
    [
        ("TERMINATE", 0x00),
        ("RANDOMISE", 0x02),
        ("COMPARE", 0x03),
        ("WITHDRAW", 0x04),
        ("QUERY SHORT ADDRESS", 0x0A),
    ],
)
def test_simple_special_commands(name, instance_byte):
    decoded_command = DALI.Decode(length=24, data=((0xC1 << 16) + (instance_byte << 8)))
    target_command = "".ljust(ADDRESS_WIDTH) + name
    assert decoded_command.cmd() == target_command, f"failed for {name}"


@pytest.mark.parametrize("opcode", [0x02, 0x03, 0x04])
def test_device_undefined_codes(opcode):
    # broadcast
    decoded_command = DALI.Decode(length=24, data=(0xFFFE00 + opcode))
    target_command = "BC DEV".ljust(ADDRESS_WIDTH) + "---"
    assert decoded_command.cmd()[: len(target_command)] == target_command
    # broadcast unadressed
    decoded_command = DALI.Decode(length=24, data=(0xFDFE00 + opcode))
    target_command = "BC DEV UN".ljust(ADDRESS_WIDTH) + "---"
    assert decoded_command.cmd()[: len(target_command)] == target_command
    # short address
    for short_address in range(0x40):
        decoded_command = DALI.Decode(
            length=24,
            data=(0x01FE00 + (short_address << 17) + opcode),
            device_type=DALI.DeviceType.LED,
        )
        target_command = f"D{short_address:02}".ljust(ADDRESS_WIDTH) + "---"
        assert decoded_command.cmd()[: len(target_command)] == target_command
    # group address
    for group_address in range(0x10):
        decoded_command = DALI.Decode(
            length=24,
            data=(0x81FE00 + (group_address << 17) + opcode),
            device_type=DALI.DeviceType.LED,
        )
        target_command = f"DG{group_address:02}".ljust(ADDRESS_WIDTH) + "---"
        assert decoded_command.cmd()[: len(target_command)] == target_command


def test_power_cycle_event():
    # undefined device
    decoded_command = DALI.Decode(length=24, data=0xFEE000)
    target_command = " ".ljust(ADDRESS_WIDTH) + "POWER CYCLE EVENT"
    assert decoded_command.cmd() == target_command
    # device with short address
    for short_address in range(0x40):
        decoded_command = DALI.Decode(
            length=24, data=(0xFEE000 + (1 << 6) + short_address)
        )
        target_command = (
            f"D{short_address:02}".ljust(ADDRESS_WIDTH) + "POWER CYCLE EVENT"
        )
        assert decoded_command.cmd() == target_command
    # device is group member
    for group_address in range(0x10):
        decoded_command = DALI.Decode(
            length=24, data=(0xFEE000 + (1 << 12) + (group_address << 7))
        )
        target_command = (
            f"DG{group_address:02}".ljust(ADDRESS_WIDTH) + "POWER CYCLE EVENT"
        )
        assert decoded_command.cmd() == target_command
    # device with group and short address
    for group_address in range(0x10):
        decoded_command = DALI.Decode(
            length=24,
            data=(
                0xFEE000
                + (1 << 12)
                + (group_address << 7)
                + (1 << 6)
                + (group_address + 1)
            ),
        )
        target_command = (
            f"DG{group_address:02} D{(group_address+1):02}".ljust(ADDRESS_WIDTH)
            + "POWER CYCLE EVENT"
        )
        assert decoded_command.cmd() == target_command


def test_event_scheme_decoding():
    # see IEC62386-103-2022 7.2.2.1 Table 3
    # eventScheme Device (0)
    for short_address in range(0x40):
        for instance_type in range(0x20):
            decoded_command = DALI.Decode(
                length=24, data=((short_address << 17) + (instance_type << 10))
            )
            target_command = (
                f"D{short_address:02},T{instance_type:02}".ljust(ADDRESS_WIDTH)
                + "EVENT DATA 0x000 = 0 = 000000000000b"
            )
            assert decoded_command.cmd() == target_command
    # eventScheme Device and Instance (2)
    for short_address in range(0x40):
        for instance_number in range(0x20):
            decoded_command = DALI.Decode(
                length=24,
                data=(short_address << 17) + (1 << 15) + (instance_number << 10),
            )
            target_command = (
                f"D{short_address:02},I{instance_number:02}".ljust(ADDRESS_WIDTH)
                + "EVENT DATA 0x000 = 0 = 000000000000b"
            )
            assert decoded_command.cmd() == target_command
    # eventScheme Device group (3)
    for device_group in range(0x20):
        for instance_type in range(0x20):
            decoded_command = DALI.Decode(
                length=24, data=(1 << 23) + (device_group << 17) + (instance_type << 10)
            )
            target_command = (
                f"DG{device_group:02},T{instance_type:02}".ljust(ADDRESS_WIDTH)
                + "EVENT DATA 0x000 = 0 = 000000000000b"
            )
            assert decoded_command.cmd() == target_command
    # eventScheme Instance (0)
    for instance_type in range(0x20):
        for instance_number in range(0x20):
            decoded_command = DALI.Decode(
                length=24,
                data=(1 << 23)
                + (instance_type << 17)
                + (1 << 15)
                + (instance_number << 10),
            )
            target_command = (
                f"T{instance_type:02},I{instance_number:02}".ljust(ADDRESS_WIDTH)
                + "EVENT DATA 0x000 = 0 = 000000000000b"
            )
            assert decoded_command.cmd() == target_command
    # eventScheme Instance (0)
    for instance_groups in range(0x20):
        for instance_types in range(0x20):
            decoded_command = DALI.Decode(
                length=24,
                data=(3 << 22) + (instance_groups << 17) + (instance_types << 10),
            )
            target_command = (
                f"IG{instance_groups:02},T{instance_types:02}".ljust(ADDRESS_WIDTH)
                + "EVENT DATA 0x000 = 0 = 000000000000b"
            )
            assert decoded_command.cmd() == target_command


def test_reserved_event_schemes():
    # see IEC62386-103-2022 7.2.2.1 Table 3
    target_command = "".ljust(ADDRESS_WIDTH) + "RESERVED EVENT"
    for upper_bits in range(0x10):
        for lower_bits in range(0x20):
            decoded_command = DALI.Decode(
                length=24,
                data=(3 << 22) + (upper_bits << 17) + (1 << 15) + (lower_bits << 10),
            )
            assert decoded_command.cmd() == target_command
    for upper_bits in range(0x8):
        for lower_bits in range(0x20):
            decoded_command = DALI.Decode(
                length=24,
                data=(7 << 21) + (upper_bits << 17) + (1 << 15) + (lower_bits << 10),
            )
            assert decoded_command.cmd() == target_command
    for upper_bits in range(0x4):
        for lower_bits in range(0x20):
            decoded_command = DALI.Decode(
                length=24,
                data=(0xF << 20) + (upper_bits << 17) + (1 << 15) + (lower_bits << 10),
            )
            assert decoded_command.cmd() == target_command
    for upper_bits in range(0x2):
        for lower_bits in range(0x20):
            decoded_command = DALI.Decode(
                length=24,
                data=(
                    (0x1F << 19) + (upper_bits << 17) + (1 << 15) + (lower_bits << 10)
                ),
            )
            assert decoded_command.cmd() == target_command


def run_thru_instance_addressing(basic_data, basic_addressing, command_name):
    for instance_number in range(0x20):
        target_command = (basic_addressing + f",I{instance_number:02}").ljust(
            ADDRESS_WIDTH
        ) + command_name
        decoded_command = DALI.Decode(
            length=24, data=basic_data + (instance_number << 8)
        )
        assert decoded_command.cmd() == target_command
    for instance_group in range(0x20):
        target_command = (basic_addressing + f",IG{instance_group:02}").ljust(
            ADDRESS_WIDTH
        ) + command_name
        decoded_command = DALI.Decode(
            length=24, data=basic_data + (instance_group << 8) + (1 << 15)
        )
        assert decoded_command.cmd() == target_command
    for instance_typ in range(0x20):
        target_command = (basic_addressing + f",T{instance_typ:02}").ljust(
            ADDRESS_WIDTH
        ) + command_name
        decoded_command = DALI.Decode(
            length=24, data=basic_data + (instance_typ << 8) + (3 << 14)
        )
        assert decoded_command.cmd() == target_command
    for instance_number in range(0x20):
        target_command = (basic_addressing + f",FI{instance_number:02}").ljust(
            ADDRESS_WIDTH
        ) + command_name
        decoded_command = DALI.Decode(
            length=24, data=basic_data + (instance_number << 8) + (1 << 13)
        )
        assert decoded_command.cmd() == target_command
    for instance_group in range(0x20):
        target_command = (basic_addressing + f",FG{instance_group:02}").ljust(
            ADDRESS_WIDTH
        ) + command_name
        decoded_command = DALI.Decode(
            length=24, data=basic_data + (instance_group << 8) + (5 << 13)
        )
        assert decoded_command.cmd() == target_command
    for instance_typ in range(0x20):
        target_command = (basic_addressing + f",FT{instance_typ:02}").ljust(
            ADDRESS_WIDTH
        ) + command_name
        decoded_command = DALI.Decode(
            length=24, data=basic_data + (instance_typ << 8) + (3 << 13)
        )
        assert decoded_command.cmd() == target_command


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
