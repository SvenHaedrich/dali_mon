from typing import Tuple
from bitstring import BitArray

# bit position translation
#
#  2222|1111||1111|11  ||    |      IEC docs
#  3210|9876||5432|1098||7654|3210
# -----+----++----+----++----+-----
#  0123|4567||8911|1111||1111|2222  BitArray index
#      |    ||  01|2345||6789|0123
#


class EventType:
    RESERVED = 0
    DEVICE = 1
    DEVICE_INSTANCE = 2
    DEVICE_GROUP = 3
    INSTANCE = 4
    INSTANCE_GROUP = 5


class InstanceAddressType:
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


class DeviceAddressType:
    RESERVED = 0
    SHORT_ADDRESS = 1
    GROUP_ADDRESS = 2
    BROADCAST_UNADDR = 3
    BROADCAST = 4
    SPECIAL = 5


class ForwardFrame24Bit:
    LENGTH = 24

    def device_command(self) -> str:
        # see iec 62386-103 11.2 table 23 - standard commands
        code_dictionary = {
            0x00: "IDENTIFY DEVICE",
            0x01: "RESET POWER CYCLE SEEN",
            0x10: "RESET",
            0x11: "RESET MEMORY BANK (DTR0)",
            0x14: "SET SHORT ADDRESS (DTR0)",
            0x15: "ENABLE WRITE MEMORY",
            0x16: "ENABLE APPLICATION CONTROLLER",
            0x17: "DISABLE APPLICATION CONTROLLER",
            0x18: "SET OPERATING MODE (DTR0)",
            0x19: "ADD TO DEVICE GROUPS 0-15 (DTR2:DTR1)",
            0x1A: "ADD TO DEVICE GROUPS 16-31 (DTR2:DTR1)",
            0x1B: "REMOVE FROM DEVICE GROUPS 0-15 (DTR2:DTR1)",
            0x1C: "REMOVE FROM DEVICE GROUPS 16-31 (DTR2:DTR1)",
            0x1D: "START QUIESCENT MODE",
            0x1E: "STOP QUIESCENT MODE",
            0x1F: "ENABLE POWER CYCLE NOTIFICATION",
            0x20: "DISABLE POWER CYCLE NOTIFICATION",
            0x21: "SAVE PERSISTENT VARIABLES (DEPRECATED)",
            0x30: "QUERY DEVICE STATUS",
            0x31: "QUERY APPLICATION CONTROLLER ERROR",
            0x32: "QUERY INPUT DEVICE ERROR",
            0x33: "QUERY MISSING SHORT ADDRESS",
            0x34: "QUERY VERSION NUMBER",
            0x35: "QUERY NUMBER OF INSTANCES",
            0x36: "QUERY CONTENT DTR0",
            0x37: "QUERY CONTENT DTR1",
            0x38: "QUERY CONTENT DTR2",
            0x39: "QUERY RANDOM ADDRESS (H)",
            0x3A: "QUERY RANDOM ADDRESS (M)",
            0x3B: "QUERY RANDOM ADDRESS (L)",
            0x3C: "READ MEMORY LOCATION (DTR1,DTR0)",
            0x3D: "QUERY APPLICATION CONTROLLER ENABLED",
            0x3E: "QUERY OPERATING MODE",
            0x3F: "QUERY MANUFACTURER SPECIFIC MODE",
            0x40: "QUERY QUIESCENT MODE",
            0x41: "QUERY DEVICE GROUPS 0-7",
            0x42: "QUERY DEVICE GROUPS 8-15",
            0x43: "QUERY DEVICE GROUPS 16-23",
            0x44: "QUERY DEVICE GROUPS 24-31",
            0x45: "QUERY POWER CYCLE NOTIFICATION",
            0x46: "QUERY DEVICE CAPABILITIES",
            0x47: "QUERY EXTENDED VERSION NUMBER (DTR0)",
            0x48: "QUERY RESET STATE",
            0x49: "QUERY APPLICATION CONTROLLER ALWAYS ACTIVE",
        }
        opcode_byte = self.frame_bits[16:].uint
        return code_dictionary.get(
            opcode_byte,
            f"--- CODE 0x{opcode_byte:02X} = {opcode_byte} UNDEFINED CONTROL DEVICE COMMAND",
        )

    def instance_commands(self) -> str:
        code_dictionary = {
            0x00: "SET SHORT TIMER (DTR0) - TYPE 301",
            0x01: "SET DOUBLE TIMER (DTR0) - TYPE 301",
            0x02: "SET REPEAT TIMER (DTR0) - TYPE 301",
            0x03: "SET STUCK TIMER (DTR0) - TYPE 301",
            0x0A: "QUERY SHORT TIMER - TYPE 301",
            0x0B: "QUERY SHORT TIMER MIN - TYPE 301",
            0x0C: "QUERY DOUBLE TIMER - TYPE 301",
            0x0D: "QUERY DOUBLE TIMER MIN - TYPE 301",
            0x0E: "QUERY REPEAT TIMER - TYPE 301",
            0x0F: "QUERY STUCK TIMER - TYPE 301",
            0x10: "SET REPORT TIMER (DTR0) - TYPE 302",
            0x11: "SET DEADTIME TIMER (DTR0) - TYPE 302",
            0x1D: "QUERY DEADTIME TIMER - TYPE 302",
            0x1E: "QUERY REPORT TIMER - TYPE 302",
            0x1F: "QUERY SWITCH - TYPE 302",
            0x20: "CATCH MOVEMENT - TYPE 303",
            0x21: "SET HOLD TIMER (DTR0) - TYPE 303",
            0x22: "SET REPORT TIMER (DTR0)- TYPE 303",
            0x23: "SET DEADTIME TIMER (DTR0) - TYPE 303",
            0x24: "CANCEL HOLD TIMER -TYPE 303",
            0x2C: "QUERY DEADTIME TIMER - TYPE 303",
            0x2D: "QUERY HOLD TIMER - TYPE 303",
            0x2E: "QUERY REPORT TIMER - TYPE 303",
            0x2F: "QUERY CACHING - TYPE 303",
            0x30: "SET REPORT TIMER (DTR0) - TYPE 304",
            0x31: "SET HYSTERESIS (DTR0) - TYPE 304",
            0x32: "SET DEADTIME TIMER (DTR0) - TYPE 304",
            0x33: "SET HYSTERESIS MIN (DTR0) - TYPE 304",
            0x3C: "QUERY HYSTERESIS MIN - TYPE 304",
            0x3D: "QUERY DEADTIME TIMER - TYPE 304",
            0x3E: "QUERY REPORT TIMER - TYPE 304",
            0x3F: "QUERY HYSTERESIS - TYPE 304",
            0x61: "SET EVENT PRIORITY (DTR0)",
            0x62: "ENABLE INSTANCE",
            0x63: "DISABLE INSTANCE",
            0x64: "SET PRIMARY INSTANCE GROUP (DTR0)",
            0x65: "SET INSTANCE GROUP 1 (DTR0)",
            0x66: "SET INSTANCE GROUP 2 (DTR0)",
            0x67: "SET EVENT SCHEME (DTR0)",
            0x68: "SET EVENT FILTER (DTR2,DTR1,DTR0)",
            0x69: "SET INSTANCE TYPE (DTR0)",
            0x6A: "SET INSTANCE CONFIGURATION (DTR0,DTR2:DTR1)",
            0x80: "QUERY INSTANCE TYPE",
            0x81: "QUERY RESOLUTION",
            0x82: "QUERY INSTANCE ERROR",
            0x83: "QUERY INSTANCE STATUS",
            0x84: "QUERY EVENT PRIORITY",
            0x86: "QUERY INSTANCE ENABLED",
            0x88: "QUERY PRIMARY INSTANCE GROUP",
            0x89: "QUERY INSTANCE GROUP 1",
            0x8A: "QUERY INSTANCE GROUP 2",
            0x8B: "QUERY EVENT SCHEME",
            0x8C: "QUERY INPUT VALUE",
            0x8D: "QUERY INPUT VALUE LATCH",
            0x8E: "QUERY FEATURE TYPE",
            0x8F: "QUERY NEXT FEATURE TYPE",
            0x90: "QUERY EVENT FILTER 0-7",
            0x91: "QUERY EVENT FILTER 8-15",
            0x92: "QUERY EVENT FILTER 16-23",
            0x93: "QUERY INSTANCE CONFIGURATION (DTR0)",
            0x94: "QUERY AVAILABLE INSTANCE TYPES",
        }
        opcode_byte = self.frame_bits[16:].uint
        return code_dictionary.get(
            opcode_byte,
            f"--- CODE 0x{opcode_byte:02X} = {opcode_byte} UNDEFINED INSTANCE COMMAND",
        )

    def device_special_command(self) -> str:
        address_byte = self.frame_bits[:8].uint
        instance_byte = self.frame_bits[8:16].uint
        opcode_byte = self.frame_bits[16:].uint
        if address_byte == 0xC1:
            if instance_byte == 0x00:
                return "TERMINATE"
            elif instance_byte == 0x01:
                # IEC 62386-103:2022 Table 25 Device addressing with INITALISE
                if opcode_byte in range(0x40):
                    return f"INITIALISE (D{opcode_byte:02})"
                if opcode_byte == 0x7F:
                    return "INITIALISE (UNADDRESSED)"
                if opcode_byte == 0xFF:
                    return "INITIALISE (ALL)"
                return f"INITIALISE (NONE) - 0x{opcode_byte:02X}"
            elif instance_byte == 0x02:
                return "RANDOMISE"
            elif instance_byte == 0x03:
                return "COMPARE"
            elif instance_byte == 0x04:
                return "WITHDRAW"
            elif instance_byte == 0x05:
                return f"SEARCHADDRH (0x{opcode_byte:02X}) = {opcode_byte}"
            elif instance_byte == 0x06:
                return f"SEARCHADDRM (0x{opcode_byte:02X}) = {opcode_byte}"
            elif instance_byte == 0x07:
                return f"SEARCHADDRL (0x{opcode_byte:02X}) = {opcode_byte}"
            elif instance_byte == 0x08:
                return f"PROGRAM SHORT ADDRESS (0x{opcode_byte:02X}) = {opcode_byte}"
            elif instance_byte == 0x09:
                return f"VERIFY SHORT ADDRESS (0x{opcode_byte:02X}) = {opcode_byte}"
            elif instance_byte == 0x0A:
                return "QUERY SHORT ADDRESS"
            elif instance_byte == 0x20:
                return f"WRITE MEMORY LOCATION DTR1, DTR0, (0x{opcode_byte:02X}) = {opcode_byte}"
            elif instance_byte == 0x21:
                return f"WRITE MEMORY LOCATION - NO REPLY - DTR1, DTR0, (0x{opcode_byte:02X}) = {opcode_byte}"
            elif instance_byte == 0x30:
                return f"DTR0 0x{opcode_byte:02X} = {opcode_byte:3} = {opcode_byte:08b}"
            elif instance_byte == 0x31:
                return f"DTR1 0x{opcode_byte:02X} = {opcode_byte:3} = {opcode_byte:08b}"
            elif instance_byte == 0x32:
                return f"DTR2 0x{opcode_byte:02X} = {opcode_byte:3} = {opcode_byte:08b}"
            elif instance_byte == 0x33:
                return f"SEND TESTFRAME (0x{opcode_byte:02X}) = {opcode_byte}"
        if address_byte == 0xC5:
            return f"DIRECT WRITE MEMORY (DTR0,0x{instance_byte:02X}) : 0x{opcode_byte:02X}"
        if address_byte == 0xC7:
            return f"DTR1:DTR0 (0x{instance_byte:02X},0x{opcode_byte:02X})"
        if address_byte == 0xC9:
            return f"DTR2:DTR1 (0x{instance_byte:02X},0x{opcode_byte:02X})"
        return f"--- CODE 0x{address_byte:02X} = {address_byte} UNKNOWN CONTROL DEVICE SPECIAL COMMAND"

    # IEC 62386-103:2022 Table 2 - instance byte in a command frame
    def get_instance_address_type(self) -> InstanceAddressType:
        instance_byte = self.frame_bits[8:16].uint
        if instance_byte == 0xFE:
            return InstanceAddressType.DEVICE
        if instance_byte == 0xFC:
            return InstanceAddressType.FEATURE_ON_DEVICE
        if instance_byte == 0xFF:
            return InstanceAddressType.INSTANCE_BROADCAST
        if instance_byte == 0xFD:
            return InstanceAddressType.FEATURE_ON_INSTANCE_BROADCAST
        if instance_byte == 0xF9:
            return InstanceAddressType.FEATURE_BROADCAST
        instance_code = self.frame_bits[8:11].uint
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
        if self.frame_bits[:8].uint == 0xFF:
            return DeviceAddressType.BROADCAST
        if self.frame_bits[:8].uint == 0xFD:
            return DeviceAddressType.BROADCAST_UNADDR
        if not self.frame_bits[0]:
            return DeviceAddressType.SHORT_ADDRESS
        if self.frame_bits[:2].uint == 0b10:
            return DeviceAddressType.GROUP_ADDRESS
        if self.frame_bits[:3].uint == 0b110:
            return DeviceAddressType.SPECIAL
        return DeviceAddressType.RESERVED

    # IEC 62386-103:2022 Table 3 - event message frame encoding
    def get_event_source_type(self) -> EventType:
        if not self.frame_bits[0]:
            if self.frame_bits[8]:
                return EventType.DEVICE_INSTANCE
            else:
                return EventType.DEVICE
        if not self.frame_bits[1]:
            if self.frame_bits[8]:
                return EventType.INSTANCE
            else:
                return EventType.DEVICE_GROUP
        else:
            if not self.frame_bits[8]:
                return EventType.INSTANCE_GROUP
        return EventType.RESERVED

    def build_command_address_string(
        self, address_type: DeviceAddressType, instance_type: InstanceAddressType
    ) -> str:
        # todo make address_type instance_type a class_member
        if address_type == DeviceAddressType.SHORT_ADDRESS:
            short_address = self.frame_bits[1:7].uint
            address_string = f"D{short_address:02}"
        elif address_type == DeviceAddressType().GROUP_ADDRESS:
            group_address = self.frame_bits[2:7].uint
            address_string = f"DG{group_address:02}"
        elif address_type == DeviceAddressType.BROADCAST_UNADDR:
            address_string = "BC DEV UN"
        elif address_type == DeviceAddressType.BROADCAST:
            address_string = "BC DEV"
        if instance_type == InstanceAddressType.INSTANCE_NUMBER:
            number = self.frame_bits[11:16].uint
            address_string += f",I{number:02}"
        elif instance_type == InstanceAddressType.INSTANCE_GROUP:
            group = self.frame_bits[11:16].uint
            address_string += f",IG{group:02}"
        elif instance_type == InstanceAddressType.INSTANCE_TYPE:
            type = self.frame_bits[11:16].uint
            address_string += f",T{type:02}"
        elif instance_type == InstanceAddressType.FEATURE_ON_INSTANCE_NUMBER:
            number = self.frame_bits[11:16].uint
            address_string += f",FI{number:02}"
        elif instance_type == InstanceAddressType.FEATURE_ON_INSTANCE_GROUP:
            group = self.frame_bits[11:16].uint
            address_string += f",FG{group:02}"
        elif instance_type == InstanceAddressType.FEATURE_ON_INSTANCE_TYPE:
            type = self.frame_bits[11:16].uint
            address_string += f",FT{type:02}"
        elif instance_type == InstanceAddressType.FEATURE_BROADCAST:
            address_string += "BC FEAT"
        elif instance_type == InstanceAddressType.FEATURE_ON_INSTANCE_BROADCAST:
            address_string += "BC FEAT INST"
        elif instance_type == InstanceAddressType.INSTANCE_BROADCAST:
            address_string += "BC INST"
        elif instance_type == InstanceAddressType.FEATURE_ON_DEVICE:
            address_string += "FEAT DEV"
        if (
            instance_type == InstanceAddressType.RESERVED
            or address_type == DeviceAddressType.RESERVED
        ):
            address_string = "RESERVED"
        return address_string

    def build_event_source_string(self, event_source_type: EventType) -> str:
        if event_source_type == EventType.DEVICE:
            short_address = self.frame_bits[1:7].uint
            instance_type = self.frame_bits[9:14].uint
            return f"D{short_address:02},T{instance_type:02}"
        elif event_source_type == EventType.DEVICE_INSTANCE:
            short_address = self.frame_bits[1:7].uint
            instance_number = self.frame_bits[9:14].uint
            return f"D{short_address:02},I{instance_number:02}"
        elif event_source_type == EventType.DEVICE_GROUP:
            device_group = self.frame_bits[2:7].uint
            instance_type = self.frame_bits[9:14].uint
            return f"DG{device_group:02},T{instance_type:02}"
        elif event_source_type == EventType.INSTANCE:
            instance_type = self.frame_bits[2:7].uint
            instance_number = self.frame_bits[9:14].uint
            return f"T{instance_type:02},I{instance_number:02}"
        elif event_source_type == EventType.INSTANCE_GROUP:
            device_group = self.frame_bits[2:7].uint
            instance_type = self.frame_bits[9:14].uint
            return f"IG{device_group:02},T{instance_type:02}"
        else:
            return ""

    def build_power_event_device(self) -> str:
        # see iec 62386-103:2022 9.7.2
        if self.frame_bits[11]:
            device_group = self.frame_bits[12:17].uint
            group_result = f"DG{device_group:02} "
        else:
            group_result = ""
        if self.frame_bits[17]:
            short_address = self.frame_bits[18:].uint
            return f"{group_result}D{short_address:02}"
        else:
            return f"{group_result}".rstrip()

    def adr(self) -> str:
        return self.address

    def cmd(self) -> str:
        return self.command

    def data(self) -> str:
        return f"{self.frame_data:06X}"

    def __init__(self, data: int) -> None:
        self.frame_bits = BitArray(uint=data, length=24)
        self.frame_data = data

        # see iec 62386-103 7.2.2.1
        if self.frame_bits[:11].uint == 0x7F7:
            self.address = self.build_power_event_device()
            self.command = "POWER CYCLE EVENT"
            return

        self.address = ""
        if not self.frame_bits[7]:
            event_source_type = self.get_event_source_type()
            if event_source_type == EventType.RESERVED:
                self.command = "RESERVED EVENT"
            else:
                self.address = self.build_event_source_string(event_source_type)
                self.command = f"EVENT DATA 0x{(data & 0x3FF):03X} = {(data & 0x3FF)} = {(data & 0x3FF):012b}b"
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
                self.command = self.device_command()
            else:
                self.command = self.instance_commands()
        if device_address_type == DeviceAddressType.SPECIAL:
            self.command = self.device_special_command()
        return
