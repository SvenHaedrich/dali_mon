import pytest
from dali_interface import DaliFrame

import dali_mon
from DALI.decode import Decode
from DALI.forward_frame_16bit import DeviceType


def reference(
    length: int, data: int, device_type: int = DeviceType.NONE
) -> tuple[str, str]:
    return Decode(DaliFrame(length=length, data=data), device_type).get_reference()


# the clauses as given in the command tables and contents of the standards
@pytest.mark.parametrize(
    "length,data,device_type,standard,clause",
    [
        pytest.param(
            8, 0x12, DeviceType.NONE, "IEC 62386-101:2022", "7.4.5", id="backward frame"
        ),
        pytest.param(
            16,
            0xFF05,
            DeviceType.NONE,
            "IEC 62386-102:2022",
            "11.3.7",
            id="RECALL MAX LEVEL",
        ),
        pytest.param(
            16,
            0x0164,
            DeviceType.NONE,
            "IEC 62386-102:2022",
            "11.4.16",
            id="ADD TO GROUP 4",
        ),
        pytest.param(
            16, 0xFE80, DeviceType.NONE, "IEC 62386-102:2022", "11.3.1", id="DAPC"
        ),
        pytest.param(
            16, 0xA100, DeviceType.NONE, "IEC 62386-102:2022", "11.7.1", id="TERMINATE"
        ),
        pytest.param(
            16,
            0xC906,
            DeviceType.NONE,
            "IEC 62386-102:2022",
            "11.7.18",
            id="WRITE MEMORY LOCATION - NO REPLY",
        ),
        pytest.param(
            16,
            0xFFE0,
            DeviceType.LED,
            "IEC 62386-207:2018",
            "11.3.2.1",
            id="DT6 REFERENCE SYSTEM POWER",
        ),
        pytest.param(
            16,
            0xFFE0,
            DeviceType.SWITCH,
            "IEC 62386-208:2009",
            "11.3.4.1",
            id="DT7 REFERENCE SYSTEM POWER",
        ),
        pytest.param(
            16,
            0xFFFA,
            DeviceType.COLOUR,
            "IEC 62386-209:2011",
            "11.3.4.3",
            id="DT8 QUERY COLOUR VALUE",
        ),
        pytest.param(
            24,
            0xFFFE00,
            DeviceType.NONE,
            "IEC 62386-103:2022",
            "11.4.2",
            id="IDENTIFY DEVICE",
        ),
        pytest.param(
            24,
            0x018062,
            DeviceType.NONE,
            "IEC 62386-103:2022",
            "11.8.2",
            id="ENABLE INSTANCE",
        ),
        pytest.param(
            24,
            0x01C100,
            DeviceType.NONE,
            "IEC 62386-301:2017",
            "11.8.3",
            id="301 SET SHORT TIMER",
        ),
        pytest.param(
            24,
            0x01C210,
            DeviceType.NONE,
            "IEC 62386-302:2017",
            "11.8.2",
            id="302 SET REPORT TIMER",
        ),
        pytest.param(
            24,
            0x01C32F,
            DeviceType.NONE,
            "IEC 62386-303:2017",
            "11.9.6",
            id="303 QUERY CATCHING",
        ),
        pytest.param(
            24,
            0x01C43F,
            DeviceType.NONE,
            "IEC 62386-304:2017",
            "11.9.5",
            id="304 QUERY HYSTERESIS",
        ),
        pytest.param(
            24,
            0xC10000,
            DeviceType.NONE,
            "IEC 62386-103:2022",
            "11.10.2",
            id="TERMINATE device",
        ),
        pytest.param(
            24,
            0xC12100,
            DeviceType.NONE,
            "IEC 62386-103:2022",
            "11.10.14",
            id="WRITE MEMORY LOCATION - NO REPLY device",
        ),
        pytest.param(
            24,
            0xC90102,
            DeviceType.NONE,
            "IEC 62386-103:2022",
            "11.10.20",
            id="DTR2:DTR1",
        ),
        pytest.param(
            24,
            0x000000,
            DeviceType.NONE,
            "IEC 62386-103:2022",
            "11.3.1",
            id="event message",
        ),
        pytest.param(
            24,
            0xFEE000,
            DeviceType.NONE,
            "IEC 62386-103:2022",
            "9.7.2",
            id="power cycle event",
        ),
        pytest.param(
            32,
            0x01FB0000,
            DeviceType.NONE,
            "IEC 62386-105:2020",
            "11.3.2.1",
            id="START FW TRANSFER",
        ),
        pytest.param(
            32,
            0xCB000000,
            DeviceType.NONE,
            "IEC 62386-105:2020",
            "11.3.3.1",
            id="BEGIN BLOCK",
        ),
        # removed in the current editions, defined in the editions of 2014
        pytest.param(
            16,
            0xFF22,
            DeviceType.NONE,
            "IEC 62386-102:2014",
            "11.4.4",
            id="SAVE PERSISTENT VARIABLES",
        ),
        pytest.param(
            24,
            0xFFFE21,
            DeviceType.NONE,
            "IEC 62386-103:2014",
            "11.5.17",
            id="SAVE PERSISTENT VARIABLES device",
        ),
    ],
)
def test_reference(length, data, device_type, standard, clause):
    assert reference(length, data, device_type) == (standard, clause)


@pytest.mark.parametrize(
    "length,data",
    [
        pytest.param(16, 0xBD00, id="PHYSICAL SELECTION deprecated"),
        pytest.param(16, 0xFF26, id="unknown gear command"),
        pytest.param(16, 0xA101, id="unknown special command"),
        pytest.param(16, 0xCC00, id="reserved address"),
        pytest.param(24, 0xE10000, id="reserved command space"),
        pytest.param(12, 0x000, id="undefined frame length"),
    ],
)
def test_no_reference(length, data):
    assert reference(length, data) == ("", "")


def test_edali():
    assert reference(25, 0x1FFFF00) == ("eDALI", "")


def all_commands():
    """Every command of the tables of the decoders, addressed by broadcast."""
    for opcode in range(0x100):
        yield 16, 0xFF00 + opcode, DeviceType.NONE
        for device_type in (DeviceType.LED, DeviceType.SWITCH, DeviceType.COLOUR):
            if opcode >= 0xE0:
                yield 16, 0xFF00 + opcode, device_type
        yield 24, 0xFFFE00 + opcode, DeviceType.NONE  # device commands
        yield 24, 0x018000 + opcode, DeviceType.NONE  # instance commands
        yield (
            32,
            0x01FB0000 + (opcode << 8),
            DeviceType.NONE,
        )  # firmware transfer commands


# a command has a standard and a clause, or neither (unknown or deprecated)
def test_references_are_complete():
    for length, data, device_type in all_commands():
        standard, clause = reference(length, data, device_type)
        command = Decode(
            DaliFrame(length=length, data=data), device_type
        ).get_strings()[2]
        assert bool(standard) == bool(clause), f"{length} bit {data:X}: {command}"
        if not standard:
            assert command.startswith("---") or "DEPRECATED" in command, (
                f"{length} bit {data:X}: {command}"
            )


# the command column has a fixed width, no command is longer
def test_command_width():
    longest = ""
    for data in range(0x10000):
        for device_type in (
            DeviceType.NONE,
            DeviceType.LED,
            DeviceType.SWITCH,
            DeviceType.COLOUR,
        ):
            command = Decode(
                DaliFrame(length=16, data=data), device_type
            ).get_strings()[2]
            longest = max(longest, command, key=len)
    for address in range(0x100):
        for instance in range(0x100):
            command = Decode(
                DaliFrame(length=24, data=(address << 16) | (instance << 8) | 0xFF)
            ).get_strings()[2]
            longest = max(longest, command, key=len)
    assert len(longest) <= dali_mon.COMMAND_WIDTH, longest
