from enum import IntEnum, unique
from typing import ClassVar

from dali_interface import DaliFrame

from .reference import (
    IEC_62386_102,
    IEC_62386_207,
    IEC_62386_208,
    IEC_62386_209,
    Command,
    Reference,
    lookup,
)


@unique
class DeviceType(IntEnum):
    NONE = 0
    LED = 6
    SWITCH = 7
    COLOUR = 8


class ForwardFrame16Bit:
    LENGTH = 16
    # iec 62386-102:2022 Table 18: reference of the special commands by address byte,
    # PHYSICAL SELECTION (0xBD) is no longer part of the standard
    SPECIAL_COMMAND_REFERENCES: ClassVar[dict[int, Reference]] = {
        0xA1: Reference(IEC_62386_102, "11.7.1"),
        0xA3: Reference(IEC_62386_102, "11.7.3"),
        0xA5: Reference(IEC_62386_102, "11.7.4"),
        0xA7: Reference(IEC_62386_102, "11.7.5"),
        0xA9: Reference(IEC_62386_102, "11.7.6"),
        0xAB: Reference(IEC_62386_102, "11.7.7"),
        0xAD: Reference(IEC_62386_102, "11.7.19"),
        0xB1: Reference(IEC_62386_102, "11.7.8"),
        0xB3: Reference(IEC_62386_102, "11.7.9"),
        0xB5: Reference(IEC_62386_102, "11.7.10"),
        0xB7: Reference(IEC_62386_102, "11.7.11"),
        0xB9: Reference(IEC_62386_102, "11.7.12"),
        0xBB: Reference(IEC_62386_102, "11.7.13"),
        0xC1: Reference(IEC_62386_102, "11.7.14"),
        0xC3: Reference(IEC_62386_102, "11.7.15"),
        0xC5: Reference(IEC_62386_102, "11.7.16"),
        0xC7: Reference(IEC_62386_102, "11.7.17"),
        0xC9: Reference(IEC_62386_102, "11.7.18"),
    }

    def gear_command(self, opcode: int) -> Command:
        # see iec 62386-102:2022 11.2
        code_dictionary = {
            0x00: Command("OFF", IEC_62386_102, "11.3.2"),
            0x01: Command("UP", IEC_62386_102, "11.3.3"),
            0x02: Command("DOWN", IEC_62386_102, "11.3.4"),
            0x03: Command("STEP UP", IEC_62386_102, "11.3.5"),
            0x04: Command("STEP DOWN", IEC_62386_102, "11.3.6"),
            0x05: Command("RECALL MAX LEVEL", IEC_62386_102, "11.3.7"),
            0x06: Command("RECALL MIN LEVEL", IEC_62386_102, "11.3.8"),
            0x07: Command("STEP DOWN AND OFF", IEC_62386_102, "11.3.9"),
            0x08: Command("ON AND STEP UP", IEC_62386_102, "11.3.10"),
            0x09: Command("ENABLE DAPC SEQUENCE", IEC_62386_102, "11.3.11"),
            0x0A: Command("GO TO LAST ACTIVE LEVEL", IEC_62386_102, "11.3.12"),
            0x0B: Command("CONTINUOUS UP", IEC_62386_102, "11.3.13"),
            0x0C: Command("CONTINUOUS DOWN", IEC_62386_102, "11.3.14"),
            0x10: Command("GO TO SCENE 0", IEC_62386_102, "11.3.15"),
            0x11: Command("GO TO SCENE 1", IEC_62386_102, "11.3.15"),
            0x12: Command("GO TO SCENE 2", IEC_62386_102, "11.3.15"),
            0x13: Command("GO TO SCENE 3", IEC_62386_102, "11.3.15"),
            0x14: Command("GO TO SCENE 4", IEC_62386_102, "11.3.15"),
            0x15: Command("GO TO SCENE 5", IEC_62386_102, "11.3.15"),
            0x16: Command("GO TO SCENE 6", IEC_62386_102, "11.3.15"),
            0x17: Command("GO TO SCENE 7", IEC_62386_102, "11.3.15"),
            0x18: Command("GO TO SCENE 8", IEC_62386_102, "11.3.15"),
            0x19: Command("GO TO SCENE 9", IEC_62386_102, "11.3.15"),
            0x1A: Command("GO TO SCENE 10", IEC_62386_102, "11.3.15"),
            0x1B: Command("GO TO SCENE 11", IEC_62386_102, "11.3.15"),
            0x1C: Command("GO TO SCENE 12", IEC_62386_102, "11.3.15"),
            0x1D: Command("GO TO SCENE 13", IEC_62386_102, "11.3.15"),
            0x1E: Command("GO TO SCENE 14", IEC_62386_102, "11.3.15"),
            0x1F: Command("GO TO SCENE 15", IEC_62386_102, "11.3.15"),
            0x20: Command("RESET", IEC_62386_102, "11.4.2"),
            0x21: Command("STORE ACTUAL LEVEL IN DTR0", IEC_62386_102, "11.4.3"),
            0x22: Command("SAVE PERSISTENT VARIABLES (DEPRECATED)"),
            0x23: Command("SET OPERATING MODE (DTR0)", IEC_62386_102, "11.4.4"),
            0x24: Command("RESET MEMORY BANK (DTR0)", IEC_62386_102, "11.4.5"),
            0x25: Command("IDENTIFY DEVICE", IEC_62386_102, "11.4.6"),
            0x2A: Command("SET MAX LEVEL (DTR0)", IEC_62386_102, "11.4.7"),
            0x2B: Command("SET MIN LEVEL (DTR0)", IEC_62386_102, "11.4.8"),
            0x2C: Command("SET SYSTEM FAILURE LEVEL (DTR0)", IEC_62386_102, "11.4.9"),
            0x2D: Command("SET POWER ON LEVEL (DTR0)", IEC_62386_102, "11.4.10"),
            0x2E: Command("SET FADE TIME (DTR0)", IEC_62386_102, "11.4.11"),
            0x2F: Command("SET FADE RATE (DTR0)", IEC_62386_102, "11.4.12"),
            0x30: Command("SET EXTENDED FADE TIME (DTR0)", IEC_62386_102, "11.4.13"),
            0x40: Command("SET SCENE (DTR0) 0", IEC_62386_102, "11.4.14"),
            0x41: Command("SET SCENE (DTR0) 1", IEC_62386_102, "11.4.14"),
            0x42: Command("SET SCENE (DTR0) 2", IEC_62386_102, "11.4.14"),
            0x43: Command("SET SCENE (DTR0) 3", IEC_62386_102, "11.4.14"),
            0x44: Command("SET SCENE (DTR0) 4", IEC_62386_102, "11.4.14"),
            0x45: Command("SET SCENE (DTR0) 5", IEC_62386_102, "11.4.14"),
            0x46: Command("SET SCENE (DTR0) 6", IEC_62386_102, "11.4.14"),
            0x47: Command("SET SCENE (DTR0) 7", IEC_62386_102, "11.4.14"),
            0x48: Command("SET SCENE (DTR0) 8", IEC_62386_102, "11.4.14"),
            0x49: Command("SET SCENE (DTR0) 9", IEC_62386_102, "11.4.14"),
            0x4A: Command("SET SCENE (DTR0) 10", IEC_62386_102, "11.4.14"),
            0x4B: Command("SET SCENE (DTR0) 11", IEC_62386_102, "11.4.14"),
            0x4C: Command("SET SCENE (DTR0) 12", IEC_62386_102, "11.4.14"),
            0x4D: Command("SET SCENE (DTR0) 13", IEC_62386_102, "11.4.14"),
            0x4E: Command("SET SCENE (DTR0) 14", IEC_62386_102, "11.4.14"),
            0x4F: Command("SET SCENE (DTR0) 15", IEC_62386_102, "11.4.14"),
            0x50: Command("REMOVE FROM SCENE 0", IEC_62386_102, "11.4.15"),
            0x51: Command("REMOVE FROM SCENE 1", IEC_62386_102, "11.4.15"),
            0x52: Command("REMOVE FROM SCENE 2", IEC_62386_102, "11.4.15"),
            0x53: Command("REMOVE FROM SCENE 3", IEC_62386_102, "11.4.15"),
            0x54: Command("REMOVE FROM SCENE 4", IEC_62386_102, "11.4.15"),
            0x55: Command("REMOVE FROM SCENE 5", IEC_62386_102, "11.4.15"),
            0x56: Command("REMOVE FROM SCENE 6", IEC_62386_102, "11.4.15"),
            0x57: Command("REMOVE FROM SCENE 7", IEC_62386_102, "11.4.15"),
            0x58: Command("REMOVE FROM SCENE 8", IEC_62386_102, "11.4.15"),
            0x59: Command("REMOVE FROM SCENE 9", IEC_62386_102, "11.4.15"),
            0x5A: Command("REMOVE FROM SCENE 10", IEC_62386_102, "11.4.15"),
            0x5B: Command("REMOVE FROM SCENE 11", IEC_62386_102, "11.4.15"),
            0x5C: Command("REMOVE FROM SCENE 12", IEC_62386_102, "11.4.15"),
            0x5D: Command("REMOVE FROM SCENE 13", IEC_62386_102, "11.4.15"),
            0x5E: Command("REMOVE FROM SCENE 14", IEC_62386_102, "11.4.15"),
            0x5F: Command("REMOVE FROM SCENE 15", IEC_62386_102, "11.4.15"),
            0x60: Command("ADD TO GROUP 0", IEC_62386_102, "11.4.16"),
            0x61: Command("ADD TO GROUP 1", IEC_62386_102, "11.4.16"),
            0x62: Command("ADD TO GROUP 2", IEC_62386_102, "11.4.16"),
            0x63: Command("ADD TO GROUP 3", IEC_62386_102, "11.4.16"),
            0x64: Command("ADD TO GROUP 4", IEC_62386_102, "11.4.16"),
            0x65: Command("ADD TO GROUP 5", IEC_62386_102, "11.4.16"),
            0x66: Command("ADD TO GROUP 6", IEC_62386_102, "11.4.16"),
            0x67: Command("ADD TO GROUP 7", IEC_62386_102, "11.4.16"),
            0x68: Command("ADD TO GROUP 8", IEC_62386_102, "11.4.16"),
            0x69: Command("ADD TO GROUP 9", IEC_62386_102, "11.4.16"),
            0x6A: Command("ADD TO GROUP 10", IEC_62386_102, "11.4.16"),
            0x6B: Command("ADD TO GROUP 11", IEC_62386_102, "11.4.16"),
            0x6C: Command("ADD TO GROUP 12", IEC_62386_102, "11.4.16"),
            0x6D: Command("ADD TO GROUP 13", IEC_62386_102, "11.4.16"),
            0x6E: Command("ADD TO GROUP 14", IEC_62386_102, "11.4.16"),
            0x6F: Command("ADD TO GROUP 15", IEC_62386_102, "11.4.16"),
            0x70: Command("REMOVE FROM GROUP 0", IEC_62386_102, "11.4.17"),
            0x71: Command("REMOVE FROM GROUP 1", IEC_62386_102, "11.4.17"),
            0x72: Command("REMOVE FROM GROUP 2", IEC_62386_102, "11.4.17"),
            0x73: Command("REMOVE FROM GROUP 3", IEC_62386_102, "11.4.17"),
            0x74: Command("REMOVE FROM GROUP 4", IEC_62386_102, "11.4.17"),
            0x75: Command("REMOVE FROM GROUP 5", IEC_62386_102, "11.4.17"),
            0x76: Command("REMOVE FROM GROUP 6", IEC_62386_102, "11.4.17"),
            0x77: Command("REMOVE FROM GROUP 7", IEC_62386_102, "11.4.17"),
            0x78: Command("REMOVE FROM GROUP 8", IEC_62386_102, "11.4.17"),
            0x79: Command("REMOVE FROM GROUP 9", IEC_62386_102, "11.4.17"),
            0x7A: Command("REMOVE FROM GROUP 10", IEC_62386_102, "11.4.17"),
            0x7B: Command("REMOVE FROM GROUP 11", IEC_62386_102, "11.4.17"),
            0x7C: Command("REMOVE FROM GROUP 12", IEC_62386_102, "11.4.17"),
            0x7D: Command("REMOVE FROM GROUP 13", IEC_62386_102, "11.4.17"),
            0x7E: Command("REMOVE FROM GROUP 14", IEC_62386_102, "11.4.17"),
            0x7F: Command("REMOVE FROM GROUP 15", IEC_62386_102, "11.4.17"),
            0x80: Command("SET SHORT ADDRESS (DTR0)", IEC_62386_102, "11.4.18"),
            0x81: Command("ENABLE WRITE MEMORY", IEC_62386_102, "11.4.19"),
            0x90: Command("QUERY STATUS", IEC_62386_102, "11.5.2"),
            0x91: Command("QUERY CONTROL GEAR PRESENT", IEC_62386_102, "11.5.3"),
            0x92: Command("QUERY LAMP FAILURE", IEC_62386_102, "11.5.4"),
            0x93: Command("QUERY LAMP POWER ON", IEC_62386_102, "11.5.6"),
            0x94: Command("QUERY LIMIT ERROR", IEC_62386_102, "11.5.7"),
            0x95: Command("QUERY RESET STATE", IEC_62386_102, "11.5.8"),
            0x96: Command("QUERY MISSING SHORT ADDRESS", IEC_62386_102, "11.5.9"),
            0x97: Command("QUERY VERSION NUMBER", IEC_62386_102, "11.5.10"),
            0x98: Command("QUERY CONTENT DTR0", IEC_62386_102, "11.5.11"),
            0x99: Command("QUERY DEVICE TYPE", IEC_62386_102, "11.5.12"),
            0x9A: Command("QUERY PHYSICAL MINIMUM", IEC_62386_102, "11.5.13"),
            0x9B: Command("QUERY POWER FAILURE", IEC_62386_102, "11.5.15"),
            0x9C: Command("QUERY CONTENT DTR1", IEC_62386_102, "11.5.16"),
            0x9D: Command("QUERY CONTENT DTR2", IEC_62386_102, "11.5.17"),
            0x9E: Command("QUERY OPERATING MODE", IEC_62386_102, "11.5.18"),
            0x9F: Command("QUERY LIGHT SOURCE TYPE", IEC_62386_102, "11.5.19"),
            0xA0: Command("QUERY ACTUAL LEVEL", IEC_62386_102, "11.5.20"),
            0xA1: Command("QUERY MAX LEVEL", IEC_62386_102, "11.5.21"),
            0xA2: Command("QUERY MIN LEVEL", IEC_62386_102, "11.5.22"),
            0xA3: Command("QUERY POWER ON LEVEL", IEC_62386_102, "11.5.23"),
            0xA4: Command("QUERY SYSTEM FAILURE LEVEL", IEC_62386_102, "11.5.24"),
            0xA5: Command("QUERY FADE TIME / FADE RATE", IEC_62386_102, "11.5.25"),
            0xA6: Command("QUERY MANUFACTURER SPECIFIC MODE", IEC_62386_102, "11.5.27"),
            0xA7: Command("QUERY NEXT DEVICE TYPE", IEC_62386_102, "11.5.13"),
            0xA8: Command("QUERY EXTENDED FADE TIME", IEC_62386_102, "11.5.26"),
            0xAA: Command("QUERY CONTROL GEAR FAILURE", IEC_62386_102, "11.5.4"),
            0xB0: Command("QUERY SCENE LEVEL 0", IEC_62386_102, "11.5.28"),
            0xB1: Command("QUERY SCENE LEVEL 1", IEC_62386_102, "11.5.28"),
            0xB2: Command("QUERY SCENE LEVEL 2", IEC_62386_102, "11.5.28"),
            0xB3: Command("QUERY SCENE LEVEL 3", IEC_62386_102, "11.5.28"),
            0xB4: Command("QUERY SCENE LEVEL 4", IEC_62386_102, "11.5.28"),
            0xB5: Command("QUERY SCENE LEVEL 5", IEC_62386_102, "11.5.28"),
            0xB6: Command("QUERY SCENE LEVEL 6", IEC_62386_102, "11.5.28"),
            0xB7: Command("QUERY SCENE LEVEL 7", IEC_62386_102, "11.5.28"),
            0xB8: Command("QUERY SCENE LEVEL 8", IEC_62386_102, "11.5.28"),
            0xB9: Command("QUERY SCENE LEVEL 9", IEC_62386_102, "11.5.28"),
            0xBA: Command("QUERY SCENE LEVEL 10", IEC_62386_102, "11.5.28"),
            0xBB: Command("QUERY SCENE LEVEL 11", IEC_62386_102, "11.5.28"),
            0xBC: Command("QUERY SCENE LEVEL 12", IEC_62386_102, "11.5.28"),
            0xBD: Command("QUERY SCENE LEVEL 13", IEC_62386_102, "11.5.28"),
            0xBE: Command("QUERY SCENE LEVEL 14", IEC_62386_102, "11.5.28"),
            0xBF: Command("QUERY SCENE LEVEL 15", IEC_62386_102, "11.5.28"),
            0xC0: Command("QUERY GROUPS 0-7", IEC_62386_102, "11.5.29"),
            0xC1: Command("QUERY GROUPS 8-15", IEC_62386_102, "11.5.30"),
            0xC2: Command("QUERY RANDOM ADDRESS (H)", IEC_62386_102, "11.5.31"),
            0xC3: Command("QUERY RANDOM ADDRESS (M)", IEC_62386_102, "11.5.32"),
            0xC4: Command("QUERY RANDOM ADDRESS (L)", IEC_62386_102, "11.5.33"),
            0xC5: Command("READ MEMORY LOCATION (DTR1,DTR0)", IEC_62386_102, "11.5.34"),
            0xFF: Command("QUERY EXTENDED VERSION NUMBER", IEC_62386_102, "11.6.2"),
        }
        return lookup(
            code_dictionary,
            opcode,
            f"--- CODE 0x{opcode:02X} = {opcode} UNKNOWN CONTROL GEAR COMMAND",
        )

    def gear_colour_command(self, opcode: int) -> Command:
        # DT 8 commands
        # iec 62386 - 209 11.3
        code_dictionary = {
            0xE0: Command("SET TEMPORARY X-COORDINATE", IEC_62386_209, "11.3.4.1"),
            0xE1: Command("SET TEMPORARY Y-COORDINATE", IEC_62386_209, "11.3.4.1"),
            0xE2: Command("ACTIVATE", IEC_62386_209, "11.3.4.1"),
            0xE3: Command("X-COORDINATE STEP UP", IEC_62386_209, "11.3.4.1"),
            0xE4: Command("X-COORDINATE STEP DOWN", IEC_62386_209, "11.3.4.1"),
            0xE5: Command("Y-COORDINATE STEP UP", IEC_62386_209, "11.3.4.1"),
            0xE6: Command("Y-COORDINATE STEP DOWN", IEC_62386_209, "11.3.4.1"),
            0xE7: Command(
                "SET TEMPORARY COLOUR TEMPERATURE TC", IEC_62386_209, "11.3.4.1"
            ),
            0xE8: Command(
                "COLOUR TEMPERATURE TC STEP COOLER", IEC_62386_209, "11.3.4.1"
            ),
            0xE9: Command(
                "COLOUR TEMPERATURE TC STEP WARMER", IEC_62386_209, "11.3.4.1"
            ),
            0xEA: Command(
                "SET TEMPORARY PRIMARY N DIMLEVEL", IEC_62386_209, "11.3.4.1"
            ),
            0xEB: Command("SET TEMPORARY RGB DIMLEVEL", IEC_62386_209, "11.3.4.1"),
            0xEC: Command("SET TEMPORARY WAF DIMLEVEL", IEC_62386_209, "11.3.4.1"),
            0xED: Command("SET TEMPORARY RGBWAF CONTROL", IEC_62386_209, "11.3.4.1"),
            0xEE: Command("COPY REPORT TO TEMPORARY", IEC_62386_209, "11.3.4.1"),
            0xF0: Command("STORE TY PRIMARY N", IEC_62386_209, "11.3.4.2"),
            0xF1: Command("STORE XY-COORDINATE PRIMARY N", IEC_62386_209, "11.3.4.2"),
            0xF2: Command(
                "STORE COLOUR TEMPERATURE TC LIMIT", IEC_62386_209, "11.3.4.2"
            ),
            0xF3: Command("STORE GEAR FEATURE/STATUS", IEC_62386_209, "11.3.4.2"),
            0xF5: Command("ASSIGN COLOUR TO LINKED CHANNEL", IEC_62386_209, "11.3.4.2"),
            0xF6: Command("START AUTO CALIBRATION", IEC_62386_209, "11.3.4.2"),
            0xF7: Command("QUERY GEAR FEATURES/STATUS", IEC_62386_209, "11.3.4.3"),
            0xF8: Command("QUERY COLOUR STATUS", IEC_62386_209, "11.3.4.3"),
            0xF9: Command("QUERY COLOUR TYPE FEATURES", IEC_62386_209, "11.3.4.3"),
            0xFA: Command("QUERY COLOUR VALUE", IEC_62386_209, "11.3.4.3"),
            0xFB: Command("QUERY RGBWAF CONTROL", IEC_62386_209, "11.3.4.3"),
            0xFC: Command("QUERY ASSIGNED COLOUR", IEC_62386_209, "11.3.4.3"),
            0xFF: Command("QUERY EXTENDED VERSION NUMBER", IEC_62386_209, "11.3.4.3"),
        }
        return lookup(
            code_dictionary,
            opcode,
            f"--- CODE 0x{opcode:02X} = {opcode} UNKNOWN COLOUR GEAR COMMAND",
        )

    def gear_switch_command(self, opcode: int) -> Command:
        # DT 7 commands
        # iec 62386 - 208 11.3.4.1
        code_dictionary = {
            0xE0: Command("REFERENCE SYSTEM POWER", IEC_62386_208, "11.3.4.1"),
            0xE1: Command(
                "STORE DTR AS UP SWITCH-ON THRESHOLD", IEC_62386_208, "11.3.4.1"
            ),
            0xE2: Command(
                "STORE DTR AS UP SWITCH-OFF THRESHOLD", IEC_62386_208, "11.3.4.1"
            ),
            0xE3: Command(
                "STORE DTR AS DOWN SWITCH-ON THRESHOLD", IEC_62386_208, "11.3.4.1"
            ),
            0xE4: Command(
                "STORE DTR AS DOWN SWITCH-OFF THRESHOLD", IEC_62386_208, "11.3.4.1"
            ),
            0xE5: Command(
                "STORE DTR AS ERROR HOLD-OFF TIME", IEC_62386_208, "11.3.4.1"
            ),
            0xF0: Command("QUERY FEATURES", IEC_62386_208, "11.3.4.2"),
            0xF1: Command("QUERY SWITCH STATUS", IEC_62386_208, "11.3.4.2"),
            0xF2: Command("QUERY UP SWITCH-ON THRESHOLD", IEC_62386_208, "11.3.4.2"),
            0xF3: Command("QUERY UP SWITCH-OFF THRESHOLD", IEC_62386_208, "11.3.4.2"),
            0xF4: Command("QUERY DOWN SWITCH-ON THRESHOLD", IEC_62386_208, "11.3.4.2"),
            0xF5: Command("QUERY DOWN SWITCH-OFF THRESHOLD", IEC_62386_208, "11.3.4.2"),
            0xF6: Command("QUERY ERROR HOLD-OFF TIME", IEC_62386_208, "11.3.4.2"),
            0xF7: Command("QUERY GEAR TYPE", IEC_62386_208, "11.3.4.2"),
            0xF9: Command("QUERY REFERENCE RUNNING", IEC_62386_208, "11.3.4.2"),
            0xFA: Command(
                "QUERY REFERENCE MEASUREMENT FAILED", IEC_62386_208, "11.3.4.2"
            ),
            0xFF: Command("QUERY EXTENDED VERSION NUMBER", IEC_62386_208, "11.3.4.2"),
        }
        return lookup(
            code_dictionary,
            opcode,
            f"--- CODE 0x{opcode:02X} = {opcode} UNKNOWN SWITCH GEAR COMMAND",
        )

    def gear_led_command(self, opcode: int) -> Command:
        # DT 6 commands
        # iec 62386 - 207 11.3
        code_dictionary = {
            0xE0: Command("REFERENCE SYSTEM POWER", IEC_62386_207, "11.3.2.1"),
            0xE3: Command("SELECT DIMMING CURVE (DTR0)", IEC_62386_207, "11.3.2.2"),
            0xE4: Command("SET FAST FADE TIME (DTR0)", IEC_62386_207, "11.3.2.3"),
            0xED: Command("QUERY CONTROL GEAR TYPE", IEC_62386_207, "11.3.3.1"),
            0xEE: Command("QUERY DIMMING CURVE", IEC_62386_207, "11.3.3.2"),
            0xF0: Command("QUERY FEATURES", IEC_62386_207, "11.3.3.3"),
            0xF1: Command("QUERY FAILURE STATUS", IEC_62386_207, "11.3.3.4"),
            0xF4: Command("QUERY LOAD DECREASE", IEC_62386_207, "11.3.3.5"),
            0xF5: Command("QUERY LOAD INCREASE", IEC_62386_207, "11.3.3.6"),
            0xF7: Command("QUERY THERMAL SHUTDOWN", IEC_62386_207, "11.3.3.7"),
            0xF8: Command("QUERY THERMAL OVERLOAD", IEC_62386_207, "11.3.3.8"),
            0xF9: Command("QUERY REFERENCE RUNNING", IEC_62386_207, "11.3.3.9"),
            0xFA: Command(
                "QUERY REFERENCE MEASUREMENT FAILED", IEC_62386_207, "11.3.3.10"
            ),
            0xFD: Command("QUERY FAST FADE TIME", IEC_62386_207, "11.3.3.11"),
            0xFE: Command("QUERY MIN FAST FADE TIME", IEC_62386_207, "11.3.3.12"),
            0xFF: Command("QUERY EXTENDED VERSION NUMBER", IEC_62386_207, "11.3.3.13"),
        }
        return lookup(
            code_dictionary,
            opcode,
            f"--- CODE 0x{opcode:02X} = {opcode} UNKNOWN LED GEAR COMMAND",
        )

    def special_command(self) -> str:
        # iec 62386-102 11.2
        if self.frame.address_byte == 0xA1 and self.frame.opcode_byte == 0x00:
            return "TERMINATE"
        elif self.frame.address_byte == 0xA3:
            return f"DTR0 0x{self.frame.opcode_byte:02X} = {self.frame.opcode_byte:3} = {self.frame.opcode_byte:08b}b"
        elif self.frame.address_byte == 0xA5:
            # iec 62386-102:2022 Table 20 Device addressing with INITIALISE
            if (
                (self.frame.opcode_byte >> 1) >= 0x00
                and (self.frame.opcode_byte >> 1) <= 0x3F
                and (self.frame.opcode_byte & 0x01)
            ):
                return f"INITIALISE (G{(self.frame.opcode_byte >> 1):02})"
            if self.frame.opcode_byte == 0xFF:
                return "INITIALISE (UNADDRESSED)"
            if self.frame.opcode_byte == 0x00:
                return "INITIALISE (ALL)"
            return f"INITIALISE (NONE) - 0x{self.frame.opcode_byte:02x}"
        elif self.frame.address_byte == 0xA7 and self.frame.opcode_byte == 0x00:
            return "RANDOMISE"
        elif self.frame.address_byte == 0xA9 and self.frame.opcode_byte == 0x00:
            return "COMPARE"
        elif self.frame.address_byte == 0xAB and self.frame.opcode_byte == 0x00:
            return "WITHDRAW"
        elif self.frame.address_byte == 0xAD and self.frame.opcode_byte == 0x00:
            return "PING"
        elif self.frame.address_byte == 0xB1:
            return f"SEARCHADDRH 0x{self.frame.opcode_byte:02X} = {self.frame.opcode_byte:3} = {self.frame.opcode_byte:08b}b"
        elif self.frame.address_byte == 0xB3:
            return f"SEARCHADDRM 0x{self.frame.opcode_byte:02X} = {self.frame.opcode_byte:3} = {self.frame.opcode_byte:08b}b"
        elif self.frame.address_byte == 0xB5:
            return f"SEARCHADDRL 0x{self.frame.opcode_byte:02X} = {self.frame.opcode_byte:3} = {self.frame.opcode_byte:08b}b"
        elif self.frame.address_byte == 0xB7:
            if (
                (self.frame.opcode_byte >> 1) >= 0x00
                and (self.frame.opcode_byte >> 1) <= 0x3F
                and (self.frame.opcode_byte & 0x01)
            ):
                short_address = self.frame.opcode_byte >> 1
                return (
                    f"PROGRAM SHORT ADDRESS (0x{short_address:02X}) = {short_address}"
                )
            return f"PROGRAM SHORT ADDRESS (none) - 0x{self.frame.opcode_byte:02X}"
        elif self.frame.address_byte == 0xB9:
            return f"VERIFY SHORT ADDRESS (0x{self.frame.opcode_byte:02X}) = {self.frame.opcode_byte}"
        elif self.frame.address_byte == 0xBB and self.frame.opcode_byte == 0x00:
            return "QUERY SHORT ADDRESS"
        elif self.frame.address_byte == 0xBD:
            return "PHYSICAL SELECTION  (DEPRECATED)"
        elif self.frame.address_byte == 0xC1:
            return f"ENABLE DEVICE TYPE {self.frame.opcode_byte}"
        elif self.frame.address_byte == 0xC3:
            return f"DTR1 0x{self.frame.opcode_byte:02X} = {self.frame.opcode_byte:3} = {self.frame.opcode_byte:08b}b"
        elif self.frame.address_byte == 0xC5:
            return f"DTR2 0x{self.frame.opcode_byte:02X} = {self.frame.opcode_byte:3} = {self.frame.opcode_byte:08b}b"
        elif self.frame.address_byte == 0xC7:
            return f"WRITE MEMORY LOCATION DTR1, DTR0, (0x{self.frame.opcode_byte:02X}) = {self.frame.opcode_byte}"
        elif self.frame.address_byte == 0xC9:
            return f"WRITE MEMORY LOCATION - NO REPLY - DTR1, DTR0, (0x{self.frame.opcode_byte:02X}) = {self.frame.opcode_byte}"
        else:
            return f"--- CODE 0x{self.frame.address_byte:02X} = {self.frame.address_byte} UNKNOWN CONTROL GEAR SPECIAL COMMAND"

    def adr(self) -> str:
        return self.address

    def cmd(self) -> str:
        return self.command

    def data(self) -> str:
        return f"{self.frame.data:04X}"

    def special_command_with_reference(self) -> Command:
        name = self.special_command()
        reference = self.SPECIAL_COMMAND_REFERENCES.get(self.frame.address_byte)
        if reference is None or name.startswith("---"):
            return Command(name)
        return Command(name, *reference)

    def __init__(self, frame: DaliFrame, device_type: int = DeviceType.NONE) -> None:
        self.frame = frame
        standard_command = True
        command = Command("")

        if (frame.address_byte & 0x01) == 0x00:
            standard_command = False
            command = Command(f"DAPC {frame.opcode_byte}", IEC_62386_102, "11.3.1")
        if frame.address_byte in range(0x80):
            short_address = frame.address_byte >> 1
            self.address = f"G{short_address:02}"
        elif frame.address_byte in range(0x80, 0xA0):
            group_address = (frame.address_byte >> 1) & 0x0F
            self.address = f"GG{group_address:02}"
        elif frame.address_byte in range(0xA0, 0xCC):
            standard_command = False
            self.address = ""
            command = self.special_command_with_reference()
        elif frame.address_byte in range(0xCC, 0xFC):
            standard_command = False
            self.address = ""
            command = Command("RESERVED")
        elif (frame.address_byte == 0xFD) or (frame.address_byte == 0xFC):
            self.address = "BC GEAR UN"
        elif (frame.address_byte == 0xFF) or (frame.address_byte == 0xFE):
            self.address = "BC GEAR"
        if standard_command:
            command = self.gear_command(frame.opcode_byte)
            if frame.opcode_byte >= 0xE0:
                if device_type == DeviceType.COLOUR:
                    command = self.gear_colour_command(frame.opcode_byte)
                elif device_type == DeviceType.SWITCH:
                    command = self.gear_switch_command(frame.opcode_byte)
                elif device_type == DeviceType.LED:
                    command = self.gear_led_command(frame.opcode_byte)
        self.command, self.standard, self.clause = command
