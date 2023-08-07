import pytest
import DALI

ADDRESS_WIDTH = 14


# TODO - make a complete test suite for all commands, for all instance addressing modes
# TODO - do this for 302, 303, 304 as well


def test_type_specific_commands():
    # undefined device
    decoded_command = DALI.Decode(length=24, data=0x010121)
    target_command = "D00,I01".ljust(ADDRESS_WIDTH) + "SET HOLD TIMER (DTR0) - TYPE 303"
    assert decoded_command.cmd() == target_command

    decoded_command = DALI.Decode(length=24, data=0x01020A)
    target_command = "D00,I02".ljust(ADDRESS_WIDTH) + "QUERY SHORT TIMER - TYPE 301"
    assert decoded_command.cmd() == target_command
