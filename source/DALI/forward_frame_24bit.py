from enum import IntEnum, unique
from typing import ClassVar

from dali_interface import DaliFrame

from .output_row import OutputRow
from .reference import (
    IEC_62386_103,
    IEC_62386_103_2014,
    IEC_62386_301,
    IEC_62386_302,
    IEC_62386_303,
    IEC_62386_304,
    Command,
    Reference,
    lookup,
)

# The fields are taken from the bytes of the frame: address_byte holds bits 23 to 16,
# instance_byte bits 15 to 8 and opcode_byte bits 7 to 0 (IEC 62386-103 bit numbers).


@unique
class EventType(IntEnum):
    RESERVED = 0
    DEVICE = 1
    DEVICE_INSTANCE = 2
    DEVICE_GROUP = 3
    INSTANCE = 4
    INSTANCE_GROUP = 5


@unique
class InstanceAddressType(IntEnum):
    RESERVED = 0
    INSTANCE_NUMBER = 1
    INSTANCE_GROUP = 2
    INSTANCE_TYPE = 3
    FEATURE_ON_INSTANCE_NUMBER = 4
    FEATURE_ON_INSTANCE_GROUP = 5
    FEATURE_ON_INSTANCE_TYPE = 6
    FEATURE_BROADCAST = 7
    FEATURE_ON_INSTANCE_BROADCAST = 8
    INSTANCE_BROADCAST = 9
    FEATURE_ON_DEVICE = 10
    DEVICE = 11


@unique
class DeviceAddressType(IntEnum):
    RESERVED = 0
    SHORT_ADDRESS = 1
    GROUP_ADDRESS = 2
    BROADCAST_UNADDR = 3
    BROADCAST = 4
    SPECIAL = 5


class ForwardFrame24Bit:
    LENGTH = 24
    # iec 62386-103:2022 Table 24: reference of the special commands, by instance byte
    # for the address byte 0xC1, by address byte for the others
    SPECIAL_COMMAND_REFERENCES: ClassVar[dict[int, Reference]] = {
        0x00: Reference(IEC_62386_103, "11.10.2"),
        0x01: Reference(IEC_62386_103, "11.10.3"),
        0x02: Reference(IEC_62386_103, "11.10.4"),
        0x03: Reference(IEC_62386_103, "11.10.5"),
        0x04: Reference(IEC_62386_103, "11.10.6"),
        0x05: Reference(IEC_62386_103, "11.10.7"),
        0x06: Reference(IEC_62386_103, "11.10.8"),
        0x07: Reference(IEC_62386_103, "11.10.9"),
        0x08: Reference(IEC_62386_103, "11.10.10"),
        0x09: Reference(IEC_62386_103, "11.10.11"),
        0x0A: Reference(IEC_62386_103, "11.10.12"),
        0x20: Reference(IEC_62386_103, "11.10.13"),
        0x21: Reference(IEC_62386_103, "11.10.14"),
        0x30: Reference(IEC_62386_103, "11.10.15"),
        0x31: Reference(IEC_62386_103, "11.10.16"),
        0x32: Reference(IEC_62386_103, "11.10.17"),
        0x33: Reference(IEC_62386_103, "11.10.21"),
    }
    SPECIAL_ADDRESS_REFERENCES: ClassVar[dict[int, Reference]] = {
        0xC5: Reference(IEC_62386_103, "11.10.18"),
        0xC7: Reference(IEC_62386_103, "11.10.19"),
        0xC9: Reference(IEC_62386_103, "11.10.20"),
    }

    def device_command(self) -> Command:
        # see iec 62386-103 11.2 table 23 - standard commands
        code_dictionary = {
            0x00: Command("IDENTIFY DEVICE", IEC_62386_103, "11.4.2"),
            0x01: Command("RESET POWER CYCLE SEEN", IEC_62386_103, "11.4.3"),
            0x10: Command("RESET", IEC_62386_103, "11.5.2"),
            0x11: Command("RESET MEMORY BANK (DTR0)", IEC_62386_103, "11.5.3"),
            0x14: Command("SET SHORT ADDRESS (DTR0)", IEC_62386_103, "11.5.4"),
            0x15: Command("ENABLE WRITE MEMORY", IEC_62386_103, "11.5.5"),
            0x16: Command("ENABLE APPLICATION CONTROLLER", IEC_62386_103, "11.5.6"),
            0x17: Command("DISABLE APPLICATION CONTROLLER", IEC_62386_103, "11.5.7"),
            0x18: Command("SET OPERATING MODE (DTR0)", IEC_62386_103, "11.5.8"),
            0x19: Command(
                "ADD TO DEVICE GROUPS 0-15 (DTR2:DTR1)", IEC_62386_103, "11.5.9"
            ),
            0x1A: Command(
                "ADD TO DEVICE GROUPS 16-31 (DTR2:DTR1)", IEC_62386_103, "11.5.10"
            ),
            0x1B: Command(
                "REMOVE FROM DEVICE GROUPS 0-15 (DTR2:DTR1)", IEC_62386_103, "11.5.11"
            ),
            0x1C: Command(
                "REMOVE FROM DEVICE GROUPS 16-31 (DTR2:DTR1)", IEC_62386_103, "11.5.12"
            ),
            0x1D: Command("START QUIESCENT MODE", IEC_62386_103, "11.5.13"),
            0x1E: Command("STOP QUIESCENT MODE", IEC_62386_103, "11.5.14"),
            0x1F: Command("ENABLE POWER CYCLE NOTIFICATION", IEC_62386_103, "11.5.15"),
            0x20: Command("DISABLE POWER CYCLE NOTIFICATION", IEC_62386_103, "11.5.16"),
            0x21: Command(
                "SAVE PERSISTENT VARIABLES (DEPRECATED)", IEC_62386_103_2014, "11.5.17"
            ),
            0x30: Command("QUERY DEVICE STATUS", IEC_62386_103, "11.6.3"),
            0x31: Command(
                "QUERY APPLICATION CONTROLLER ERROR", IEC_62386_103, "11.6.4"
            ),
            0x32: Command("QUERY INPUT DEVICE ERROR", IEC_62386_103, "11.6.5"),
            0x33: Command("QUERY MISSING SHORT ADDRESS", IEC_62386_103, "11.6.6"),
            0x34: Command("QUERY VERSION NUMBER", IEC_62386_103, "11.6.7"),
            0x35: Command("QUERY NUMBER OF INSTANCES", IEC_62386_103, "11.6.9"),
            0x36: Command("QUERY CONTENT DTR0", IEC_62386_103, "11.6.8"),
            0x37: Command("QUERY CONTENT DTR1", IEC_62386_103, "11.6.10"),
            0x38: Command("QUERY CONTENT DTR2", IEC_62386_103, "11.6.11"),
            0x39: Command("QUERY RANDOM ADDRESS (H)", IEC_62386_103, "11.6.12"),
            0x3A: Command("QUERY RANDOM ADDRESS (M)", IEC_62386_103, "11.6.13"),
            0x3B: Command("QUERY RANDOM ADDRESS (L)", IEC_62386_103, "11.6.14"),
            0x3C: Command("READ MEMORY LOCATION (DTR1,DTR0)", IEC_62386_103, "11.6.15"),
            0x3D: Command(
                "QUERY APPLICATION CONTROLLER ENABLED", IEC_62386_103, "11.6.16"
            ),
            0x3E: Command("QUERY OPERATING MODE", IEC_62386_103, "11.6.17"),
            0x3F: Command("QUERY MANUFACTURER SPECIFIC MODE", IEC_62386_103, "11.6.18"),
            0x40: Command("QUERY QUIESCENT MODE", IEC_62386_103, "11.6.19"),
            0x41: Command("QUERY DEVICE GROUPS 0-7", IEC_62386_103, "11.6.20"),
            0x42: Command("QUERY DEVICE GROUPS 8-15", IEC_62386_103, "11.6.21"),
            0x43: Command("QUERY DEVICE GROUPS 16-23", IEC_62386_103, "11.6.22"),
            0x44: Command("QUERY DEVICE GROUPS 24-31", IEC_62386_103, "11.6.23"),
            0x45: Command("QUERY POWER CYCLE NOTIFICATION", IEC_62386_103, "11.6.24"),
            0x46: Command("QUERY DEVICE CAPABILITIES", IEC_62386_103, "11.6.2"),
            0x47: Command(
                "QUERY EXTENDED VERSION NUMBER (DTR0)", IEC_62386_103, "11.6.25"
            ),
            0x48: Command("QUERY RESET STATE", IEC_62386_103, "11.6.26"),
            0x49: Command(
                "QUERY APPLICATION CONTROLLER ALWAYS ACTIVE", IEC_62386_103, "11.6.27"
            ),
        }
        return lookup(
            code_dictionary,
            self.frame.opcode_byte,
            f"--- CODE 0x{self.frame.opcode_byte:02X} = {self.frame.opcode_byte} UNDEFINED CONTROL DEVICE COMMAND",
        )

    def instance_commands(self) -> Command:
        code_dictionary = {
            0x00: Command("SET SHORT TIMER (DTR0) - TYPE 301", IEC_62386_301, "11.8.3"),
            0x01: Command(
                "SET DOUBLE TIMER (DTR0) - TYPE 301", IEC_62386_301, "11.8.4"
            ),
            0x02: Command(
                "SET REPEAT TIMER (DTR0) - TYPE 301", IEC_62386_301, "11.8.5"
            ),
            0x03: Command("SET STUCK TIMER (DTR0) - TYPE 301", IEC_62386_301, "11.8.6"),
            0x0A: Command("QUERY SHORT TIMER - TYPE 301", IEC_62386_301, "11.9.3"),
            0x0B: Command("QUERY SHORT TIMER MIN - TYPE 301", IEC_62386_301, "11.9.4"),
            0x0C: Command("QUERY DOUBLE TIMER - TYPE 301", IEC_62386_301, "11.9.5"),
            0x0D: Command("QUERY DOUBLE TIMER MIN - TYPE 301", IEC_62386_301, "11.9.6"),
            0x0E: Command("QUERY REPEAT TIMER - TYPE 301", IEC_62386_301, "11.9.7"),
            0x0F: Command("QUERY STUCK TIMER - TYPE 301", IEC_62386_301, "11.9.8"),
            0x10: Command(
                "SET REPORT TIMER (DTR0) - TYPE 302", IEC_62386_302, "11.8.2"
            ),
            0x11: Command(
                "SET DEADTIME TIMER (DTR0) - TYPE 302", IEC_62386_302, "11.8.3"
            ),
            0x1D: Command("QUERY DEADTIME TIMER - TYPE 302", IEC_62386_302, "11.9.3"),
            0x1E: Command("QUERY REPORT TIMER - TYPE 302", IEC_62386_302, "11.9.4"),
            0x1F: Command("QUERY SWITCH - TYPE 302", IEC_62386_302, "11.9.5"),
            0x20: Command("CATCH MOVEMENT - TYPE 303", IEC_62386_303, "11.7.2"),
            0x21: Command("SET HOLD TIMER (DTR0) - TYPE 303", IEC_62386_303, "11.8.3"),
            0x22: Command(
                "SET REPORT TIMER (DTR0) - TYPE 303", IEC_62386_303, "11.8.4"
            ),
            0x23: Command(
                "SET DEADTIME TIMER (DTR0) - TYPE 303", IEC_62386_303, "11.8.5"
            ),
            0x24: Command("CANCEL HOLD TIMER - TYPE 303", IEC_62386_303, "11.7.3"),
            0x2C: Command("QUERY DEADTIME TIMER - TYPE 303", IEC_62386_303, "11.9.3"),
            0x2D: Command("QUERY HOLD TIMER - TYPE 303", IEC_62386_303, "11.9.4"),
            0x2E: Command("QUERY REPORT TIMER - TYPE 303", IEC_62386_303, "11.9.5"),
            0x2F: Command("QUERY CATCHING - TYPE 303", IEC_62386_303, "11.9.6"),
            0x30: Command(
                "SET REPORT TIMER (DTR0) - TYPE 304", IEC_62386_304, "11.8.3"
            ),
            0x31: Command("SET HYSTERESIS (DTR0) - TYPE 304", IEC_62386_304, "11.8.4"),
            0x32: Command(
                "SET DEADTIME TIMER (DTR0) - TYPE 304", IEC_62386_304, "11.8.5"
            ),
            0x33: Command(
                "SET HYSTERESIS MIN (DTR0) - TYPE 304", IEC_62386_304, "11.8.6"
            ),
            0x3C: Command("QUERY HYSTERESIS MIN - TYPE 304", IEC_62386_304, "11.9.6"),
            0x3D: Command("QUERY DEADTIME TIMER - TYPE 304", IEC_62386_304, "11.9.2"),
            0x3E: Command("QUERY REPORT TIMER - TYPE 304", IEC_62386_304, "11.9.4"),
            0x3F: Command("QUERY HYSTERESIS - TYPE 304", IEC_62386_304, "11.9.5"),
            0x61: Command("SET EVENT PRIORITY (DTR0)", IEC_62386_103, "11.8.8"),
            0x62: Command("ENABLE INSTANCE", IEC_62386_103, "11.8.2"),
            0x63: Command("DISABLE INSTANCE", IEC_62386_103, "11.8.3"),
            0x64: Command("SET PRIMARY INSTANCE GROUP (DTR0)", IEC_62386_103, "11.8.4"),
            0x65: Command("SET INSTANCE GROUP 1 (DTR0)", IEC_62386_103, "11.8.5"),
            0x66: Command("SET INSTANCE GROUP 2 (DTR0)", IEC_62386_103, "11.8.6"),
            0x67: Command("SET EVENT SCHEME (DTR0)", IEC_62386_103, "11.8.7"),
            0x68: Command("SET EVENT FILTER (DTR2,DTR1,DTR0)", IEC_62386_103, "11.8.9"),
            0x69: Command("SET INSTANCE TYPE (DTR0)", IEC_62386_103, "11.8.10"),
            0x6A: Command(
                "SET INSTANCE CONFIGURATION (DTR0,DTR2:DTR1)", IEC_62386_103, "11.8.11"
            ),
            0x80: Command("QUERY INSTANCE TYPE", IEC_62386_103, "11.9.2"),
            0x81: Command("QUERY RESOLUTION", IEC_62386_103, "11.9.3"),
            0x82: Command("QUERY INSTANCE ERROR", IEC_62386_103, "11.9.4"),
            0x83: Command("QUERY INSTANCE STATUS", IEC_62386_103, "11.9.5"),
            0x84: Command("QUERY EVENT PRIORITY", IEC_62386_103, "11.9.13"),
            0x86: Command("QUERY INSTANCE ENABLED", IEC_62386_103, "11.9.6"),
            0x88: Command("QUERY PRIMARY INSTANCE GROUP", IEC_62386_103, "11.9.7"),
            0x89: Command("QUERY INSTANCE GROUP 1", IEC_62386_103, "11.9.8"),
            0x8A: Command("QUERY INSTANCE GROUP 2", IEC_62386_103, "11.9.9"),
            0x8B: Command("QUERY EVENT SCHEME", IEC_62386_103, "11.9.10"),
            0x8C: Command("QUERY INPUT VALUE", IEC_62386_103, "11.9.11"),
            0x8D: Command("QUERY INPUT VALUE LATCH", IEC_62386_103, "11.9.12"),
            0x8E: Command("QUERY FEATURE TYPE", IEC_62386_103, "11.9.14"),
            0x8F: Command("QUERY NEXT FEATURE TYPE", IEC_62386_103, "11.9.15"),
            0x90: Command("QUERY EVENT FILTER 0-7", IEC_62386_103, "11.9.16"),
            0x91: Command("QUERY EVENT FILTER 8-15", IEC_62386_103, "11.9.17"),
            0x92: Command("QUERY EVENT FILTER 16-23", IEC_62386_103, "11.9.18"),
            0x93: Command(
                "QUERY INSTANCE CONFIGURATION (DTR0)", IEC_62386_103, "11.9.19"
            ),
            0x94: Command("QUERY AVAILABLE INSTANCE TYPES", IEC_62386_103, "11.9.20"),
        }
        return lookup(
            code_dictionary,
            self.frame.opcode_byte,
            f"--- CODE 0x{self.frame.opcode_byte:02X} = {self.frame.opcode_byte} UNDEFINED INSTANCE COMMAND",
        )

    def device_special_command(self) -> str:
        if self.frame.address_byte == 0xC1:
            if self.frame.instance_byte == 0x00:
                return "TERMINATE"
            elif self.frame.instance_byte == 0x01:
                # IEC 62386-103:2022 Table 25 Device addressing with INITIALISE
                if self.frame.opcode_byte in range(0x40):
                    return f"INITIALISE (D{self.frame.opcode_byte:02})"
                if self.frame.opcode_byte == 0x7F:
                    return "INITIALISE (UNADDRESSED)"
                if self.frame.opcode_byte == 0xFF:
                    return "INITIALISE (ALL)"
                return f"INITIALISE (NONE) - 0x{self.frame.opcode_byte:02X}"
            elif self.frame.instance_byte == 0x02:
                return "RANDOMISE"
            elif self.frame.instance_byte == 0x03:
                return "COMPARE"
            elif self.frame.instance_byte == 0x04:
                return "WITHDRAW"
            elif self.frame.instance_byte == 0x05:
                return f"SEARCHADDRH (0x{self.frame.opcode_byte:02X}) = {self.frame.opcode_byte}"
            elif self.frame.instance_byte == 0x06:
                return f"SEARCHADDRM (0x{self.frame.opcode_byte:02X}) = {self.frame.opcode_byte}"
            elif self.frame.instance_byte == 0x07:
                return f"SEARCHADDRL (0x{self.frame.opcode_byte:02X}) = {self.frame.opcode_byte}"
            elif self.frame.instance_byte == 0x08:
                return f"PROGRAM SHORT ADDRESS (0x{self.frame.opcode_byte:02X}) = {self.frame.opcode_byte}"
            elif self.frame.instance_byte == 0x09:
                return f"VERIFY SHORT ADDRESS (0x{self.frame.opcode_byte:02X}) = {self.frame.opcode_byte}"
            elif self.frame.instance_byte == 0x0A:
                return "QUERY SHORT ADDRESS"
            elif self.frame.instance_byte == 0x20:
                return f"WRITE MEMORY LOCATION DTR1, DTR0, (0x{self.frame.opcode_byte:02X}) = {self.frame.opcode_byte}"
            elif self.frame.instance_byte == 0x21:
                return f"WRITE MEMORY LOCATION - NO REPLY - DTR1, DTR0, (0x{self.frame.opcode_byte:02X}) = {self.frame.opcode_byte}"
            elif self.frame.instance_byte == 0x30:
                return f"DTR0 0x{self.frame.opcode_byte:02X} = {self.frame.opcode_byte:3} = {self.frame.opcode_byte:08b}"
            elif self.frame.instance_byte == 0x31:
                return f"DTR1 0x{self.frame.opcode_byte:02X} = {self.frame.opcode_byte:3} = {self.frame.opcode_byte:08b}"
            elif self.frame.instance_byte == 0x32:
                return f"DTR2 0x{self.frame.opcode_byte:02X} = {self.frame.opcode_byte:3} = {self.frame.opcode_byte:08b}"
            elif self.frame.instance_byte == 0x33:
                return f"SEND TESTFRAME (0x{self.frame.opcode_byte:02X}) = {self.frame.opcode_byte}"
        if self.frame.address_byte == 0xC5:
            return f"DIRECT WRITE MEMORY (DTR0,0x{self.frame.instance_byte:02X}) : 0x{self.frame.opcode_byte:02X}"
        if self.frame.address_byte == 0xC7:
            return f"DTR1:DTR0 (0x{self.frame.instance_byte:02X},0x{self.frame.opcode_byte:02X})"
        if self.frame.address_byte == 0xC9:
            return f"DTR2:DTR1 (0x{self.frame.instance_byte:02X},0x{self.frame.opcode_byte:02X})"
        return f"--- CODE 0x{self.frame.address_byte:02X} = {self.frame.address_byte} UNKNOWN CONTROL DEVICE SPECIAL COMMAND"

    # IEC 62386-103:2022 Table 2 - instance byte in a command frame
    def get_instance_address_type(self) -> InstanceAddressType:
        if self.frame.instance_byte == 0xFE:
            return InstanceAddressType.DEVICE
        if self.frame.instance_byte == 0xFC:
            return InstanceAddressType.FEATURE_ON_DEVICE
        if self.frame.instance_byte == 0xFF:
            return InstanceAddressType.INSTANCE_BROADCAST
        if self.frame.instance_byte == 0xFD:
            return InstanceAddressType.FEATURE_ON_INSTANCE_BROADCAST
        if self.frame.instance_byte == 0xF9:
            return InstanceAddressType.FEATURE_BROADCAST
        instance_code = self.frame.instance_byte >> 5
        if instance_code == 0:
            return InstanceAddressType.INSTANCE_NUMBER
        if instance_code == 1:
            return InstanceAddressType.FEATURE_ON_INSTANCE_NUMBER
        if instance_code == 3:
            return InstanceAddressType.FEATURE_ON_INSTANCE_TYPE
        if instance_code == 4:
            return InstanceAddressType.INSTANCE_GROUP
        if instance_code == 5:
            return InstanceAddressType.FEATURE_ON_INSTANCE_GROUP
        if instance_code == 6:
            return InstanceAddressType.INSTANCE_TYPE
        return InstanceAddressType.RESERVED

    # IEC 62386-103:2022 Table 1 - command frame encoding
    def get_device_address_type(self) -> DeviceAddressType:
        if self.frame.address_byte == 0xFF:
            return DeviceAddressType.BROADCAST
        if self.frame.address_byte == 0xFD:
            return DeviceAddressType.BROADCAST_UNADDR
        if not self.frame.address_byte & 0x80:
            return DeviceAddressType.SHORT_ADDRESS
        if self.frame.address_byte >> 6 == 0b10:
            return DeviceAddressType.GROUP_ADDRESS
        if self.frame.address_byte >> 5 == 0b110:
            return DeviceAddressType.SPECIAL
        return DeviceAddressType.RESERVED

    # IEC 62386-103:2022 Table 3 - event message frame encoding
    def get_event_source_type(self) -> EventType:
        if not self.frame.address_byte & 0x80:
            if self.frame.instance_byte & 0x80:
                return EventType.DEVICE_INSTANCE
            else:
                return EventType.DEVICE
        if not self.frame.address_byte & 0x40:
            if self.frame.instance_byte & 0x80:
                return EventType.INSTANCE
            else:
                return EventType.DEVICE_GROUP
        else:
            if not self.frame.instance_byte & 0x80:
                return EventType.INSTANCE_GROUP
        return EventType.RESERVED

    def build_command_address_string(
        self, address_type: DeviceAddressType, instance_type: InstanceAddressType
    ) -> str:
        # todo make address_type instance_type a class_member
        address_string = ""
        if address_type == DeviceAddressType.SHORT_ADDRESS:
            short_address = (self.frame.address_byte >> 1) & 0x3F
            address_string = f"D{short_address:02}"
        elif address_type == DeviceAddressType.GROUP_ADDRESS:
            group_address = (self.frame.address_byte >> 1) & 0x1F
            address_string = f"DG{group_address:02}"
        elif address_type == DeviceAddressType.BROADCAST_UNADDR:
            address_string = "BC DEV UN"
        elif address_type == DeviceAddressType.BROADCAST:
            address_string = "BC DEV"
        if instance_type == InstanceAddressType.INSTANCE_NUMBER:
            number = self.frame.instance_byte & 0x1F
            address_string += f",I{number:02}"
        elif instance_type == InstanceAddressType.INSTANCE_GROUP:
            group = self.frame.instance_byte & 0x1F
            address_string += f",IG{group:02}"
        elif instance_type == InstanceAddressType.INSTANCE_TYPE:
            type = self.frame.instance_byte & 0x1F
            address_string += f",T{type:02}"
        elif instance_type == InstanceAddressType.FEATURE_ON_INSTANCE_NUMBER:
            number = self.frame.instance_byte & 0x1F
            address_string += f",FI{number:02}"
        elif instance_type == InstanceAddressType.FEATURE_ON_INSTANCE_GROUP:
            group = self.frame.instance_byte & 0x1F
            address_string += f",FG{group:02}"
        elif instance_type == InstanceAddressType.FEATURE_ON_INSTANCE_TYPE:
            type = self.frame.instance_byte & 0x1F
            address_string += f",FT{type:02}"
        elif instance_type == InstanceAddressType.FEATURE_BROADCAST:
            address_string += ",BC FEAT"
        elif instance_type == InstanceAddressType.FEATURE_ON_INSTANCE_BROADCAST:
            address_string += ",BC FEAT INST"
        elif instance_type == InstanceAddressType.INSTANCE_BROADCAST:
            address_string += ",BC INST"
        elif instance_type == InstanceAddressType.FEATURE_ON_DEVICE:
            address_string += ",FEAT DEV"
        if (
            instance_type == InstanceAddressType.RESERVED
            or address_type == DeviceAddressType.RESERVED
        ):
            address_string = "RESERVED"
        return address_string

    def build_event_source_string(self, event_source_type: EventType) -> str:
        if event_source_type == EventType.DEVICE:
            short_address = (self.frame.address_byte >> 1) & 0x3F
            instance_type = (self.frame.instance_byte >> 2) & 0x1F
            return f"D{short_address:02},T{instance_type:02}"
        elif event_source_type == EventType.DEVICE_INSTANCE:
            short_address = (self.frame.address_byte >> 1) & 0x3F
            instance_number = (self.frame.instance_byte >> 2) & 0x1F
            return f"D{short_address:02},I{instance_number:02}"
        elif event_source_type == EventType.DEVICE_GROUP:
            device_group = (self.frame.address_byte >> 1) & 0x1F
            instance_type = (self.frame.instance_byte >> 2) & 0x1F
            return f"DG{device_group:02},T{instance_type:02}"
        elif event_source_type == EventType.INSTANCE:
            instance_type = (self.frame.address_byte >> 1) & 0x1F
            instance_number = (self.frame.instance_byte >> 2) & 0x1F
            return f"T{instance_type:02},I{instance_number:02}"
        elif event_source_type == EventType.INSTANCE_GROUP:
            device_group = (self.frame.address_byte >> 1) & 0x1F
            instance_type = (self.frame.instance_byte >> 2) & 0x1F
            return f"IG{device_group:02},T{instance_type:02}"
        else:
            return ""

    def build_power_event_device(self) -> str:
        # see iec 62386-103:2022 9.7.2
        if self.frame.instance_byte & 0x10:
            device_group = (self.frame.data >> 7) & 0x1F
            group_result = f"DG{device_group:02} "
        else:
            group_result = ""
        if self.frame.opcode_byte & 0x40:
            short_address = self.frame.opcode_byte & 0x3F
            return f"{group_result}D{short_address:02}"
        else:
            return f"{group_result}".rstrip()

    def special_command_with_reference(self) -> Command:
        name = self.device_special_command()
        if self.frame.address_byte == 0xC1:
            reference = self.SPECIAL_COMMAND_REFERENCES.get(self.frame.instance_byte)
        else:
            reference = self.SPECIAL_ADDRESS_REFERENCES.get(self.frame.address_byte)
        if reference is None or name.startswith("---"):
            return Command(name)
        return Command(name, *reference)

    def __init__(self, frame: DaliFrame) -> None:
        self.frame = frame
        self.clause = ""
        self.standard = ""

        # see iec 62386-103 7.2.2.1
        if self.frame.data >> 13 == 0x7F7:
            self.address = self.build_power_event_device()
            self.command = "POWER CYCLE EVENT"
            self.standard, self.clause = IEC_62386_103, "9.7.2"
            return

        self.address = ""
        if not self.frame.address_byte & 0x01:
            event_source_type = self.get_event_source_type()
            if event_source_type == EventType.RESERVED:
                self.command = "RESERVED EVENT"
            else:
                self.address = self.build_event_source_string(event_source_type)
                self.command = f"EVENT DATA 0x{(frame.data & 0x3FF):03X} = {(frame.data & 0x3FF)} = {(frame.data & 0x3FF):012b}b"
                # the event message is the INPUT NOTIFICATION command
                self.standard, self.clause = IEC_62386_103, "11.3.1"
            return

        if (
            (self.frame.address_byte >> 4 == 0xE)
            or (self.frame.address_byte >> 3 == 0x1E)
            or (self.frame.address_byte >> 2 == 0x3E)
        ):
            self.command = "RESERVED"
            return

        instance_address_type = self.get_instance_address_type()
        device_address_type = self.get_device_address_type()
        if (
            (device_address_type == DeviceAddressType.SHORT_ADDRESS)
            or (device_address_type == DeviceAddressType.GROUP_ADDRESS)
            or (device_address_type == DeviceAddressType.BROADCAST)
            or (device_address_type == DeviceAddressType.BROADCAST_UNADDR)
        ):
            self.address = self.build_command_address_string(
                device_address_type, instance_address_type
            )
            if instance_address_type == InstanceAddressType.DEVICE:
                command = self.device_command()
            else:
                command = self.instance_commands()
            self.command, self.standard, self.clause = command
        if device_address_type == DeviceAddressType.SPECIAL:
            command = self.special_command_with_reference()
            self.command, self.standard, self.clause = command

    def output_row(self) -> OutputRow:
        return OutputRow(
            f"{self.frame.data:06X}",
            self.address,
            self.command,
            self.standard,
            self.clause,
        )
