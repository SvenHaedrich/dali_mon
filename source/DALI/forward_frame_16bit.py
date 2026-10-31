from enum import IntEnum, unique
from typing import ClassVar

from dali_interface import DaliFrame

from .decoded_frame import (
    IEC_62386_102,
    IEC_62386_102_2014,
    IEC_62386_207,
    IEC_62386_208,
    IEC_62386_209,
    DecodedFrame,
)


@unique
class DeviceType(IntEnum):
    NONE = 0
    LED = 6
    SWITCH = 7
    COLOUR = 8


class ForwardFrame16Bit(DecodedFrame):
    LENGTH = 16
    DATA_DIGITS = 4
    # iec 62386-102:2022 Table 18: reference of the special commands by address byte,
    # PHYSICAL SELECTION (0xBD) is no longer part of the standard
    SPECIAL_COMMAND_REFERENCES: ClassVar[dict[int, tuple[str, str]]] = {
        0xA1: (IEC_62386_102, "11.7.1"),
        0xA3: (IEC_62386_102, "11.7.3"),
        0xA5: (IEC_62386_102, "11.7.4"),
        0xA7: (IEC_62386_102, "11.7.5"),
        0xA9: (IEC_62386_102, "11.7.6"),
        0xAB: (IEC_62386_102, "11.7.7"),
        0xAD: (IEC_62386_102, "11.7.19"),
        0xB1: (IEC_62386_102, "11.7.8"),
        0xB3: (IEC_62386_102, "11.7.9"),
        0xB5: (IEC_62386_102, "11.7.10"),
        0xB7: (IEC_62386_102, "11.7.11"),
        0xB9: (IEC_62386_102, "11.7.12"),
        0xBB: (IEC_62386_102, "11.7.13"),
        0xC1: (IEC_62386_102, "11.7.14"),
        0xC3: (IEC_62386_102, "11.7.15"),
        0xC5: (IEC_62386_102, "11.7.16"),
        0xC7: (IEC_62386_102, "11.7.17"),
        0xC9: (IEC_62386_102, "11.7.18"),
    }

    def gear_command(self, opcode: int) -> tuple[str, str, str]:
        # see iec 62386-102:2022 11.2
        code_dictionary = {
            0x00: ("OFF", IEC_62386_102, "11.3.2"),
            0x01: ("UP", IEC_62386_102, "11.3.3"),
            0x02: ("DOWN", IEC_62386_102, "11.3.4"),
            0x03: ("STEP UP", IEC_62386_102, "11.3.5"),
            0x04: ("STEP DOWN", IEC_62386_102, "11.3.6"),
            0x05: ("RECALL MAX LEVEL", IEC_62386_102, "11.3.7"),
            0x06: ("RECALL MIN LEVEL", IEC_62386_102, "11.3.8"),
            0x07: ("STEP DOWN AND OFF", IEC_62386_102, "11.3.9"),
            0x08: ("ON AND STEP UP", IEC_62386_102, "11.3.10"),
            0x09: ("ENABLE DAPC SEQUENCE", IEC_62386_102, "11.3.11"),
            0x0A: ("GO TO LAST ACTIVE LEVEL", IEC_62386_102, "11.3.12"),
            0x0B: ("CONTINUOUS UP", IEC_62386_102, "11.3.13"),
            0x0C: ("CONTINUOUS DOWN", IEC_62386_102, "11.3.14"),
            0x10: ("GO TO SCENE 0", IEC_62386_102, "11.3.15"),
            0x11: ("GO TO SCENE 1", IEC_62386_102, "11.3.15"),
            0x12: ("GO TO SCENE 2", IEC_62386_102, "11.3.15"),
            0x13: ("GO TO SCENE 3", IEC_62386_102, "11.3.15"),
            0x14: ("GO TO SCENE 4", IEC_62386_102, "11.3.15"),
            0x15: ("GO TO SCENE 5", IEC_62386_102, "11.3.15"),
            0x16: ("GO TO SCENE 6", IEC_62386_102, "11.3.15"),
            0x17: ("GO TO SCENE 7", IEC_62386_102, "11.3.15"),
            0x18: ("GO TO SCENE 8", IEC_62386_102, "11.3.15"),
            0x19: ("GO TO SCENE 9", IEC_62386_102, "11.3.15"),
            0x1A: ("GO TO SCENE 10", IEC_62386_102, "11.3.15"),
            0x1B: ("GO TO SCENE 11", IEC_62386_102, "11.3.15"),
            0x1C: ("GO TO SCENE 12", IEC_62386_102, "11.3.15"),
            0x1D: ("GO TO SCENE 13", IEC_62386_102, "11.3.15"),
            0x1E: ("GO TO SCENE 14", IEC_62386_102, "11.3.15"),
            0x1F: ("GO TO SCENE 15", IEC_62386_102, "11.3.15"),
            0x20: ("RESET", IEC_62386_102, "11.4.2"),
            0x21: ("STORE ACTUAL LEVEL IN DTR0", IEC_62386_102, "11.4.3"),
            0x22: (
                "SAVE PERSISTENT VARIABLES (DEPRECATED)",
                IEC_62386_102_2014,
                "11.4.4",
            ),
            0x23: ("SET OPERATING MODE (DTR0)", IEC_62386_102, "11.4.4"),
            0x24: ("RESET MEMORY BANK (DTR0)", IEC_62386_102, "11.4.5"),
            0x25: ("IDENTIFY DEVICE", IEC_62386_102, "11.4.6"),
            0x2A: ("SET MAX LEVEL (DTR0)", IEC_62386_102, "11.4.7"),
            0x2B: ("SET MIN LEVEL (DTR0)", IEC_62386_102, "11.4.8"),
            0x2C: ("SET SYSTEM FAILURE LEVEL (DTR0)", IEC_62386_102, "11.4.9"),
            0x2D: ("SET POWER ON LEVEL (DTR0)", IEC_62386_102, "11.4.10"),
            0x2E: ("SET FADE TIME (DTR0)", IEC_62386_102, "11.4.11"),
            0x2F: ("SET FADE RATE (DTR0)", IEC_62386_102, "11.4.12"),
            0x30: ("SET EXTENDED FADE TIME (DTR0)", IEC_62386_102, "11.4.13"),
            0x40: ("SET SCENE (DTR0) 0", IEC_62386_102, "11.4.14"),
            0x41: ("SET SCENE (DTR0) 1", IEC_62386_102, "11.4.14"),
            0x42: ("SET SCENE (DTR0) 2", IEC_62386_102, "11.4.14"),
            0x43: ("SET SCENE (DTR0) 3", IEC_62386_102, "11.4.14"),
            0x44: ("SET SCENE (DTR0) 4", IEC_62386_102, "11.4.14"),
            0x45: ("SET SCENE (DTR0) 5", IEC_62386_102, "11.4.14"),
            0x46: ("SET SCENE (DTR0) 6", IEC_62386_102, "11.4.14"),
            0x47: ("SET SCENE (DTR0) 7", IEC_62386_102, "11.4.14"),
            0x48: ("SET SCENE (DTR0) 8", IEC_62386_102, "11.4.14"),
            0x49: ("SET SCENE (DTR0) 9", IEC_62386_102, "11.4.14"),
            0x4A: ("SET SCENE (DTR0) 10", IEC_62386_102, "11.4.14"),
            0x4B: ("SET SCENE (DTR0) 11", IEC_62386_102, "11.4.14"),
            0x4C: ("SET SCENE (DTR0) 12", IEC_62386_102, "11.4.14"),
            0x4D: ("SET SCENE (DTR0) 13", IEC_62386_102, "11.4.14"),
            0x4E: ("SET SCENE (DTR0) 14", IEC_62386_102, "11.4.14"),
            0x4F: ("SET SCENE (DTR0) 15", IEC_62386_102, "11.4.14"),
            0x50: ("REMOVE FROM SCENE 0", IEC_62386_102, "11.4.15"),
            0x51: ("REMOVE FROM SCENE 1", IEC_62386_102, "11.4.15"),
            0x52: ("REMOVE FROM SCENE 2", IEC_62386_102, "11.4.15"),
            0x53: ("REMOVE FROM SCENE 3", IEC_62386_102, "11.4.15"),
            0x54: ("REMOVE FROM SCENE 4", IEC_62386_102, "11.4.15"),
            0x55: ("REMOVE FROM SCENE 5", IEC_62386_102, "11.4.15"),
            0x56: ("REMOVE FROM SCENE 6", IEC_62386_102, "11.4.15"),
            0x57: ("REMOVE FROM SCENE 7", IEC_62386_102, "11.4.15"),
            0x58: ("REMOVE FROM SCENE 8", IEC_62386_102, "11.4.15"),
            0x59: ("REMOVE FROM SCENE 9", IEC_62386_102, "11.4.15"),
            0x5A: ("REMOVE FROM SCENE 10", IEC_62386_102, "11.4.15"),
            0x5B: ("REMOVE FROM SCENE 11", IEC_62386_102, "11.4.15"),
            0x5C: ("REMOVE FROM SCENE 12", IEC_62386_102, "11.4.15"),
            0x5D: ("REMOVE FROM SCENE 13", IEC_62386_102, "11.4.15"),
            0x5E: ("REMOVE FROM SCENE 14", IEC_62386_102, "11.4.15"),
            0x5F: ("REMOVE FROM SCENE 15", IEC_62386_102, "11.4.15"),
            0x60: ("ADD TO GROUP 0", IEC_62386_102, "11.4.16"),
            0x61: ("ADD TO GROUP 1", IEC_62386_102, "11.4.16"),
            0x62: ("ADD TO GROUP 2", IEC_62386_102, "11.4.16"),
            0x63: ("ADD TO GROUP 3", IEC_62386_102, "11.4.16"),
            0x64: ("ADD TO GROUP 4", IEC_62386_102, "11.4.16"),
            0x65: ("ADD TO GROUP 5", IEC_62386_102, "11.4.16"),
            0x66: ("ADD TO GROUP 6", IEC_62386_102, "11.4.16"),
            0x67: ("ADD TO GROUP 7", IEC_62386_102, "11.4.16"),
            0x68: ("ADD TO GROUP 8", IEC_62386_102, "11.4.16"),
            0x69: ("ADD TO GROUP 9", IEC_62386_102, "11.4.16"),
            0x6A: ("ADD TO GROUP 10", IEC_62386_102, "11.4.16"),
            0x6B: ("ADD TO GROUP 11", IEC_62386_102, "11.4.16"),
            0x6C: ("ADD TO GROUP 12", IEC_62386_102, "11.4.16"),
            0x6D: ("ADD TO GROUP 13", IEC_62386_102, "11.4.16"),
            0x6E: ("ADD TO GROUP 14", IEC_62386_102, "11.4.16"),
            0x6F: ("ADD TO GROUP 15", IEC_62386_102, "11.4.16"),
            0x70: ("REMOVE FROM GROUP 0", IEC_62386_102, "11.4.17"),
            0x71: ("REMOVE FROM GROUP 1", IEC_62386_102, "11.4.17"),
            0x72: ("REMOVE FROM GROUP 2", IEC_62386_102, "11.4.17"),
            0x73: ("REMOVE FROM GROUP 3", IEC_62386_102, "11.4.17"),
            0x74: ("REMOVE FROM GROUP 4", IEC_62386_102, "11.4.17"),
            0x75: ("REMOVE FROM GROUP 5", IEC_62386_102, "11.4.17"),
            0x76: ("REMOVE FROM GROUP 6", IEC_62386_102, "11.4.17"),
            0x77: ("REMOVE FROM GROUP 7", IEC_62386_102, "11.4.17"),
            0x78: ("REMOVE FROM GROUP 8", IEC_62386_102, "11.4.17"),
            0x79: ("REMOVE FROM GROUP 9", IEC_62386_102, "11.4.17"),
            0x7A: ("REMOVE FROM GROUP 10", IEC_62386_102, "11.4.17"),
            0x7B: ("REMOVE FROM GROUP 11", IEC_62386_102, "11.4.17"),
            0x7C: ("REMOVE FROM GROUP 12", IEC_62386_102, "11.4.17"),
            0x7D: ("REMOVE FROM GROUP 13", IEC_62386_102, "11.4.17"),
            0x7E: ("REMOVE FROM GROUP 14", IEC_62386_102, "11.4.17"),
            0x7F: ("REMOVE FROM GROUP 15", IEC_62386_102, "11.4.17"),
            0x80: ("SET SHORT ADDRESS (DTR0)", IEC_62386_102, "11.4.18"),
            0x81: ("ENABLE WRITE MEMORY", IEC_62386_102, "11.4.19"),
            0x90: ("QUERY STATUS", IEC_62386_102, "11.5.2"),
            0x91: ("QUERY CONTROL GEAR PRESENT", IEC_62386_102, "11.5.3"),
            0x92: ("QUERY LAMP FAILURE", IEC_62386_102, "11.5.4"),
            0x93: ("QUERY LAMP POWER ON", IEC_62386_102, "11.5.6"),
            0x94: ("QUERY LIMIT ERROR", IEC_62386_102, "11.5.7"),
            0x95: ("QUERY RESET STATE", IEC_62386_102, "11.5.8"),
            0x96: ("QUERY MISSING SHORT ADDRESS", IEC_62386_102, "11.5.9"),
            0x97: ("QUERY VERSION NUMBER", IEC_62386_102, "11.5.10"),
            0x98: ("QUERY CONTENT DTR0", IEC_62386_102, "11.5.11"),
            0x99: ("QUERY DEVICE TYPE", IEC_62386_102, "11.5.12"),
            0x9A: ("QUERY PHYSICAL MINIMUM", IEC_62386_102, "11.5.13"),
            0x9B: ("QUERY POWER FAILURE", IEC_62386_102, "11.5.15"),
            0x9C: ("QUERY CONTENT DTR1", IEC_62386_102, "11.5.16"),
            0x9D: ("QUERY CONTENT DTR2", IEC_62386_102, "11.5.17"),
            0x9E: ("QUERY OPERATING MODE", IEC_62386_102, "11.5.18"),
            0x9F: ("QUERY LIGHT SOURCE TYPE", IEC_62386_102, "11.5.19"),
            0xA0: ("QUERY ACTUAL LEVEL", IEC_62386_102, "11.5.20"),
            0xA1: ("QUERY MAX LEVEL", IEC_62386_102, "11.5.21"),
            0xA2: ("QUERY MIN LEVEL", IEC_62386_102, "11.5.22"),
            0xA3: ("QUERY POWER ON LEVEL", IEC_62386_102, "11.5.23"),
            0xA4: ("QUERY SYSTEM FAILURE LEVEL", IEC_62386_102, "11.5.24"),
            0xA5: ("QUERY FADE TIME / FADE RATE", IEC_62386_102, "11.5.25"),
            0xA6: ("QUERY MANUFACTURER SPECIFIC MODE", IEC_62386_102, "11.5.27"),
            0xA7: ("QUERY NEXT DEVICE TYPE", IEC_62386_102, "11.5.13"),
            0xA8: ("QUERY EXTENDED FADE TIME", IEC_62386_102, "11.5.26"),
            0xAA: ("QUERY CONTROL GEAR FAILURE", IEC_62386_102, "11.5.4"),
            0xB0: ("QUERY SCENE LEVEL 0", IEC_62386_102, "11.5.28"),
            0xB1: ("QUERY SCENE LEVEL 1", IEC_62386_102, "11.5.28"),
            0xB2: ("QUERY SCENE LEVEL 2", IEC_62386_102, "11.5.28"),
            0xB3: ("QUERY SCENE LEVEL 3", IEC_62386_102, "11.5.28"),
            0xB4: ("QUERY SCENE LEVEL 4", IEC_62386_102, "11.5.28"),
            0xB5: ("QUERY SCENE LEVEL 5", IEC_62386_102, "11.5.28"),
            0xB6: ("QUERY SCENE LEVEL 6", IEC_62386_102, "11.5.28"),
            0xB7: ("QUERY SCENE LEVEL 7", IEC_62386_102, "11.5.28"),
            0xB8: ("QUERY SCENE LEVEL 8", IEC_62386_102, "11.5.28"),
            0xB9: ("QUERY SCENE LEVEL 9", IEC_62386_102, "11.5.28"),
            0xBA: ("QUERY SCENE LEVEL 10", IEC_62386_102, "11.5.28"),
            0xBB: ("QUERY SCENE LEVEL 11", IEC_62386_102, "11.5.28"),
            0xBC: ("QUERY SCENE LEVEL 12", IEC_62386_102, "11.5.28"),
            0xBD: ("QUERY SCENE LEVEL 13", IEC_62386_102, "11.5.28"),
            0xBE: ("QUERY SCENE LEVEL 14", IEC_62386_102, "11.5.28"),
            0xBF: ("QUERY SCENE LEVEL 15", IEC_62386_102, "11.5.28"),
            0xC0: ("QUERY GROUPS 0-7", IEC_62386_102, "11.5.29"),
            0xC1: ("QUERY GROUPS 8-15", IEC_62386_102, "11.5.30"),
            0xC2: ("QUERY RANDOM ADDRESS (H)", IEC_62386_102, "11.5.31"),
            0xC3: ("QUERY RANDOM ADDRESS (M)", IEC_62386_102, "11.5.32"),
            0xC4: ("QUERY RANDOM ADDRESS (L)", IEC_62386_102, "11.5.33"),
            0xC5: ("READ MEMORY LOCATION (DTR1,DTR0)", IEC_62386_102, "11.5.34"),
            0xFF: ("QUERY EXTENDED VERSION NUMBER", IEC_62386_102, "11.6.2"),
        }
        return self.lookup(
            code_dictionary,
            opcode,
            f"--- CODE 0x{opcode:02X} = {opcode} UNKNOWN CONTROL GEAR COMMAND",
        )

    def gear_colour_command(self, opcode: int) -> tuple[str, str, str]:
        # DT 8 commands
        # iec 62386 - 209 11.3
        code_dictionary = {
            0xE0: ("SET TEMPORARY X-COORDINATE", IEC_62386_209, "11.3.4.1"),
            0xE1: ("SET TEMPORARY Y-COORDINATE", IEC_62386_209, "11.3.4.1"),
            0xE2: ("ACTIVATE", IEC_62386_209, "11.3.4.1"),
            0xE3: ("X-COORDINATE STEP UP", IEC_62386_209, "11.3.4.1"),
            0xE4: ("X-COORDINATE STEP DOWN", IEC_62386_209, "11.3.4.1"),
            0xE5: ("Y-COORDINATE STEP UP", IEC_62386_209, "11.3.4.1"),
            0xE6: ("Y-COORDINATE STEP DOWN", IEC_62386_209, "11.3.4.1"),
            0xE7: ("SET TEMPORARY COLOUR TEMPERATURE TC", IEC_62386_209, "11.3.4.1"),
            0xE8: ("COLOUR TEMPERATURE TC STEP COOLER", IEC_62386_209, "11.3.4.1"),
            0xE9: ("COLOUR TEMPERATURE TC STEP WARMER", IEC_62386_209, "11.3.4.1"),
            0xEA: ("SET TEMPORARY PRIMARY N DIMLEVEL", IEC_62386_209, "11.3.4.1"),
            0xEB: ("SET TEMPORARY RGB DIMLEVEL", IEC_62386_209, "11.3.4.1"),
            0xEC: ("SET TEMPORARY WAF DIMLEVEL", IEC_62386_209, "11.3.4.1"),
            0xED: ("SET TEMPORARY RGBWAF CONTROL", IEC_62386_209, "11.3.4.1"),
            0xEE: ("COPY REPORT TO TEMPORARY", IEC_62386_209, "11.3.4.1"),
            0xF0: ("STORE TY PRIMARY N", IEC_62386_209, "11.3.4.2"),
            0xF1: ("STORE XY-COORDINATE PRIMARY N", IEC_62386_209, "11.3.4.2"),
            0xF2: ("STORE COLOUR TEMPERATURE TC LIMIT", IEC_62386_209, "11.3.4.2"),
            0xF3: ("STORE GEAR FEATURE/STATUS", IEC_62386_209, "11.3.4.2"),
            0xF5: ("ASSIGN COLOUR TO LINKED CHANNEL", IEC_62386_209, "11.3.4.2"),
            0xF6: ("START AUTO CALIBRATION", IEC_62386_209, "11.3.4.2"),
            0xF7: ("QUERY GEAR FEATURES/STATUS", IEC_62386_209, "11.3.4.3"),
            0xF8: ("QUERY COLOUR STATUS", IEC_62386_209, "11.3.4.3"),
            0xF9: ("QUERY COLOUR TYPE FEATURES", IEC_62386_209, "11.3.4.3"),
            0xFA: ("QUERY COLOUR VALUE", IEC_62386_209, "11.3.4.3"),
            0xFB: ("QUERY RGBWAF CONTROL", IEC_62386_209, "11.3.4.3"),
            0xFC: ("QUERY ASSIGNED COLOUR", IEC_62386_209, "11.3.4.3"),
            0xFF: ("QUERY EXTENDED VERSION NUMBER", IEC_62386_209, "11.3.4.3"),
        }
        return self.lookup(
            code_dictionary,
            opcode,
            f"--- CODE 0x{opcode:02X} = {opcode} UNKNOWN COLOUR GEAR COMMAND",
        )

    def gear_switch_command(self, opcode: int) -> tuple[str, str, str]:
        # DT 7 commands
        # iec 62386 - 208 11.3.4.1
        code_dictionary = {
            0xE0: ("REFERENCE SYSTEM POWER", IEC_62386_208, "11.3.4.1"),
            0xE1: ("STORE DTR AS UP SWITCH-ON THRESHOLD", IEC_62386_208, "11.3.4.1"),
            0xE2: ("STORE DTR AS UP SWITCH-OFF THRESHOLD", IEC_62386_208, "11.3.4.1"),
            0xE3: ("STORE DTR AS DOWN SWITCH-ON THRESHOLD", IEC_62386_208, "11.3.4.1"),
            0xE4: ("STORE DTR AS DOWN SWITCH-OFF THRESHOLD", IEC_62386_208, "11.3.4.1"),
            0xE5: ("STORE DTR AS ERROR HOLD-OFF TIME", IEC_62386_208, "11.3.4.1"),
            0xF0: ("QUERY FEATURES", IEC_62386_208, "11.3.4.2"),
            0xF1: ("QUERY SWITCH STATUS", IEC_62386_208, "11.3.4.2"),
            0xF2: ("QUERY UP SWITCH-ON THRESHOLD", IEC_62386_208, "11.3.4.2"),
            0xF3: ("QUERY UP SWITCH-OFF THRESHOLD", IEC_62386_208, "11.3.4.2"),
            0xF4: ("QUERY DOWN SWITCH-ON THRESHOLD", IEC_62386_208, "11.3.4.2"),
            0xF5: ("QUERY DOWN SWITCH-OFF THRESHOLD", IEC_62386_208, "11.3.4.2"),
            0xF6: ("QUERY ERROR HOLD-OFF TIME", IEC_62386_208, "11.3.4.2"),
            0xF7: ("QUERY GEAR TYPE", IEC_62386_208, "11.3.4.2"),
            0xF9: ("QUERY REFERENCE RUNNING", IEC_62386_208, "11.3.4.2"),
            0xFA: ("QUERY REFERENCE MEASUREMENT FAILED", IEC_62386_208, "11.3.4.2"),
            0xFF: ("QUERY EXTENDED VERSION NUMBER", IEC_62386_208, "11.3.4.2"),
        }
        return self.lookup(
            code_dictionary,
            opcode,
            f"--- CODE 0x{opcode:02X} = {opcode} UNKNOWN SWITCH GEAR COMMAND",
        )

    def gear_led_command(self, opcode: int) -> tuple[str, str, str]:
        # DT 6 commands
        # iec 62386 - 207 11.3
        code_dictionary = {
            0xE0: ("REFERENCE SYSTEM POWER", IEC_62386_207, "11.3.2.1"),
            0xE3: ("SELECT DIMMING CURVE (DTR0)", IEC_62386_207, "11.3.2.2"),
            0xE4: ("SET FAST FADE TIME (DTR0)", IEC_62386_207, "11.3.2.3"),
            0xED: ("QUERY CONTROL GEAR TYPE", IEC_62386_207, "11.3.3.1"),
            0xEE: ("QUERY DIMMING CURVE", IEC_62386_207, "11.3.3.2"),
            0xF0: ("QUERY FEATURES", IEC_62386_207, "11.3.3.3"),
            0xF1: ("QUERY FAILURE STATUS", IEC_62386_207, "11.3.3.4"),
            0xF4: ("QUERY LOAD DECREASE", IEC_62386_207, "11.3.3.5"),
            0xF5: ("QUERY LOAD INCREASE", IEC_62386_207, "11.3.3.6"),
            0xF7: ("QUERY THERMAL SHUTDOWN", IEC_62386_207, "11.3.3.7"),
            0xF8: ("QUERY THERMAL OVERLOAD", IEC_62386_207, "11.3.3.8"),
            0xF9: ("QUERY REFERENCE RUNNING", IEC_62386_207, "11.3.3.9"),
            0xFA: ("QUERY REFERENCE MEASUREMENT FAILED", IEC_62386_207, "11.3.3.10"),
            0xFD: ("QUERY FAST FADE TIME", IEC_62386_207, "11.3.3.11"),
            0xFE: ("QUERY MIN FAST FADE TIME", IEC_62386_207, "11.3.3.12"),
            0xFF: ("QUERY EXTENDED VERSION NUMBER", IEC_62386_207, "11.3.3.13"),
        }
        return self.lookup(
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

    def special_command_with_reference(self) -> tuple[str, str, str]:
        name = self.special_command()
        reference = self.SPECIAL_COMMAND_REFERENCES.get(self.frame.address_byte)
        if reference is None or name.startswith("---"):
            return (name, "", "")
        return (name, *reference)

    def __init__(self, frame: DaliFrame, device_type: int = DeviceType.NONE) -> None:
        super().__init__(frame)
        standard_command = True
        command = ("", "", "")

        if (frame.address_byte & 0x01) == 0x00:
            standard_command = False
            command = (f"DAPC {frame.opcode_byte}", IEC_62386_102, "11.3.1")
        if frame.address_byte in range(0x80):
            short_address = frame.address_byte >> 1
            self._address = f"G{short_address:02}"
        elif frame.address_byte in range(0x80, 0xA0):
            group_address = (frame.address_byte >> 1) & 0x0F
            self._address = f"GG{group_address:02}"
        elif frame.address_byte in range(0xA0, 0xCC):
            standard_command = False
            self._address = ""
            command = self.special_command_with_reference()
        elif frame.address_byte in range(0xCC, 0xFC):
            standard_command = False
            self._address = ""
            command = ("RESERVED", "", "")
        elif (frame.address_byte == 0xFD) or (frame.address_byte == 0xFC):
            self._address = "BC GEAR UN"
        elif (frame.address_byte == 0xFF) or (frame.address_byte == 0xFE):
            self._address = "BC GEAR"
        if standard_command:
            command = self.gear_command(frame.opcode_byte)
            if frame.opcode_byte >= 0xE0:
                if device_type == DeviceType.COLOUR:
                    command = self.gear_colour_command(frame.opcode_byte)
                elif device_type == DeviceType.SWITCH:
                    command = self.gear_switch_command(frame.opcode_byte)
                elif device_type == DeviceType.LED:
                    command = self.gear_led_command(frame.opcode_byte)
        self._command, self._standard, self._clause = command
