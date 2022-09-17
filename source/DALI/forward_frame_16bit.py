class DeviceType:
    NONE = 0
    LED = 6
    SWITCH = 7
    COLOUR = 8


class ForwardFrame16Bit:

    def gear_command(self, opcode):
        # see iec 62386-102 11.2
        code_dictionary = {
            0x00: "OFF",
            0x01: "UP",
            0x02: "DOWN",
            0x03: "STEP UP",
            0x04: "STEP DOWN",
            0x05: "RECALL MAX LEVEL",
            0x06: "RECALL MIN LEVEL",
            0x07: "STEP DOWN AND OFF",
            0x08: "ON AND STEP UP",
            0x09: "ENABLE DAPC SEQUENCE",
            0x0A: "GO TO LAST ACTIVE LEVEL",
            0x10: "GO TO SCENE 0",
            0x11: "GO TO SCENE 1",
            0x12: "GO TO SCENE 2",
            0x13: "GO TO SCENE 3",
            0x14: "GO TO SCENE 4",
            0x15: "GO TO SCENE 5",
            0x16: "GO TO SCENE 6",
            0x17: "GO TO SCENE 7",
            0x18: "GO TO SCENE 8",
            0x19: "GO TO SCENE 9",
            0x1a: "GO TO SCENE 10",
            0x1b: "GO TO SCENE 11",
            0x1c: "GO TO SCENE 12",
            0x1d: "GO TO SCENE 13",
            0x1e: "GO TO SCENE 14",
            0x1f: "GO TO SCENE 15",
            0x20: "RESET",
            0x21: "STORE ACTUAL LEVEL IN DTR0",
            0x22: "SAVE PERSISTENT VARIABLES",
            0x23: "SET OPERATING MODE (DTR0)",
            0x24: "RESET MEMORY BANK (DTR0)",
            0x25: "IDENTIFY DEVICE",
            0x2A: "SET MAX LEVEL (DTR0)",
            0x2B: "SET MIN LEVEL (DTR0)",
            0x2C: "SET SYSTEM FAILURE LEVEL (DTR0)",
            0x2D: "SET SYSTEM POWER ON LEVEL (DTR0)",
            0x2E: "SET FADE TIME (DTR0)",
            0x2F: "SET FADE RATE (DTR0)",
            0x30: "SET EXTENDED FADE TIME (DTR0)",
            0x40: "SET SCENE (DTR0) 0",
            0x41: "SET SCENE (DTR0) 1",
            0x42: "SET SCENE (DTR0) 2",
            0x43: "SET SCENE (DTR0) 3",
            0x44: "SET SCENE (DTR0) 4",
            0x45: "SET SCENE (DTR0) 5",
            0x46: "SET SCENE (DTR0) 6",
            0x47: "SET SCENE (DTR0) 7",
            0x48: "SET SCENE (DTR0) 8",
            0x49: "SET SCENE (DTR0) 9",
            0x4A: "SET SCENE (DTR0) 10",
            0x4B: "SET SCENE (DTR0) 11",
            0x4C: "SET SCENE (DTR0) 12",
            0x4D: "SET SCENE (DTR0) 13",
            0x4E: "SET SCENE (DTR0) 14",
            0x4F: "SET SCENE (DTR0) 15",
            0x50: "REMOVE FROM SCENE 0",
            0x51: "REMOVE FROM SCENE 1",
            0x52: "REMOVE FROM SCENE 2",
            0x53: "REMOVE FROM SCENE 3",
            0x54: "REMOVE FROM SCENE 4",
            0x55: "REMOVE FROM SCENE 5",
            0x56: "REMOVE FROM SCENE 6",
            0x57: "REMOVE FROM SCENE 7",
            0x58: "REMOVE FROM SCENE 8",
            0x59: "REMOVE FROM SCENE 9",
            0x5A: "REMOVE FROM SCENE 10",
            0x5B: "REMOVE FROM SCENE 11",
            0x5C: "REMOVE FROM SCENE 12",
            0x5D: "REMOVE FROM SCENE 13",
            0x5E: "REMOVE FROM SCENE 14",
            0x5F: "REMOVE FROM SCENE 15",
            0x60: "ADD TO GROUP 0",
            0x61: "ADD TO GROUP 1",
            0x62: "ADD TO GROUP 2",
            0x63: "ADD TO GROUP 3",
            0x64: "ADD TO GROUP 4",
            0x65: "ADD TO GROUP 5",
            0x66: "ADD TO GROUP 6",
            0x67: "ADD TO GROUP 7",
            0x68: "ADD TO GROUP 8",
            0x69: "ADD TO GROUP 9",
            0x6A: "ADD TO GROUP 10",
            0x6B: "ADD TO GROUP 11",
            0x6C: "ADD TO GROUP 12",
            0x6D: "ADD TO GROUP 13",
            0x6E: "ADD TO GROUP 14",
            0x6F: "ADD TO GROUP 15",
            0x70: "REMOVE FROM GROUP 0",
            0x71: "REMOVE FROM GROUP 1",
            0x72: "REMOVE FROM GROUP 2",
            0x73: "REMOVE FROM GROUP 3",
            0x74: "REMOVE FROM GROUP 4",
            0x75: "REMOVE FROM GROUP 5",
            0x76: "REMOVE FROM GROUP 6",
            0x77: "REMOVE FROM GROUP 7",
            0x78: "REMOVE FROM GROUP 8",
            0x79: "REMOVE FROM GROUP 9",
            0x7A: "REMOVE FROM GROUP 10",
            0x7B: "REMOVE FROM GROUP 11",
            0x7C: "REMOVE FROM GROUP 12",
            0x7D: "REMOVE FROM GROUP 13",
            0x7E: "REMOVE FROM GROUP 14",
            0x7F: "REMOVE FROM GROUP 15",
            0x80: "SET SHORT ADDRESS (DTR0)",
            0x81: "ENABLE WRITE MEMORY",
            0x90: "QUERY STATUS",
            0x91: "QUERY CONTROL GEAR PRESENT",
            0x92: "QUERY LAMP FAILURE",
            0x93: "QUERY LAMP POWER ON",
            0x94: "QUERY LIMIT ERROR",
            0x95: "QUERY RESET STATE",
            0x96: "QUERY MISSING SHORT ADDRESS",
            0x97: "QUERY VERSION NUMBER",
            0x98: "QUERY CONTENT DTR0",
            0x99: "QUERY DEVICE TYPE",
            0x9A: "QUERY PHYSICAL MINIMUM",
            0x9B: "QUERY POWER FAILURE",
            0x9C: "QUERY CONTENT DTR1",
            0x9D: "QUERY CONTENT DTR2",
            0x9E: "QUERY OPERATING MODE",
            0x9F: "QUERY LIGHT SOURCE TYPE",
            0xA0: "QUERY ACTUAL LEVEL",
            0xA1: "QUERY MAX LEVEL",
            0XA2: "QUERY MIN LEVEL",
            0xA3: "QUERY POWER ON LEVEL",
            0xA4: "QUERY SYSTEM FAILURE LEVEL",
            0xA5: "QUERY FADE TIME / FADE RATE",
            0xA6: "QUERY MANUFACTURER SPECIFIC MODE",
            0xA7: "QUERY NEXT DEVICE TYPE",
            0xA8: "QUERY EXTENDED FADE TIME",
            0xAA: "QUERY CONTROL GEAR FAILURE",
            0xB0: "QUERY SCENE LEVEL 0",
            0xB1: "QUERY SCENE LEVEL 1",
            0xB2: "QUERY SCENE LEVEL 2",
            0xB3: "QUERY SCENE LEVEL 3",
            0xB4: "QUERY SCENE LEVEL 4",
            0xB5: "QUERY SCENE LEVEL 5",
            0xB6: "QUERY SCENE LEVEL 6",
            0xB7: "QUERY SCENE LEVEL 7",
            0xB8: "QUERY SCENE LEVEL 8",
            0xB9: "QUERY SCENE LEVEL 9",
            0xBA: "QUERY SCENE LEVEL 10",
            0xBB: "QUERY SCENE LEVEL 11",
            0xBC: "QUERY SCENE LEVEL 12",
            0xBD: "QUERY SCENE LEVEL 13",
            0xBE: "QUERY SCENE LEVEL 14",
            0xBF: "QUERY SCENE LEVEL 15",
            0xC0: "QUERY GROUPS 0-7",
            0xC1: "QUERY GROUPS 8-15",
            0xC2: "QUERY RANDOM ADDRESS (H)",
            0xC3: "QUERY RANDOM ADDRESS (M)",
            0xC4: "QUERY RANDOM ADDRESS (L)",
            0xC5: "READ MEMORY LOCATION (DTR1,DTR0)",
            0xFF: "QUERY EXTENDED VERSION NUMBER"
        }
        if opcode in code_dictionary:
            return code_dictionary.get(opcode)
        else:
            return F"--- CODE 0x{opcode:02X} = {opcode} UNKNOWN CONTROL GEAR COMMAND"

    def gear_colour_command(self, opcode):
        # DT 8 commands
        # iec 62386 - 209 11.3
        code_dictionary = {
            0xE0: "SET TEMPORARY X-COORDINATE",
            0xE1: "SET TEMPORARY Y-COORDINATE",
            0xE2: "ACTIVATE",
            0xE3: "X-COORDINATE STEP UP",
            0XE4: "X-COORDINATE STEP DOWN",
            0xE5: "Y-COORDINATE STEP UP",
            0xE6: "Y-COORDINATE STEP DOWN",
            0xE7: "SET TEMPORARY COLOUR TEMPERATURE TC",
            0xE8: "COLOUR TEMPERATURE TC STEP COOLER",
            0xE9: "COLOUR TEMPERTAURE TC STEP WARMER",
            0xEA: "SET TEMPORARY PRIMARY N DIMLEVEL",
            0xEB: "SET TEMPORARY RGB DIMLEVEL",
            0xEC: "SET TEMPORARY WAF DIMLEVEL",
            0xED: "SET TEMPORARY RGBWAF CONTROL",
            0xEE: "COPY REPORT TO TEMPORARY",
            0xF0: "STORE TY PRIMARY N",
            0xF1: "STORE XY-COORDINATE PRIMARY N",
            0xF2: "STORE COLOUR TEMPERATURE TC LIMIT",
            0xF3: "STORE GEAR FEATURE/STATUS",
            0xF5: "ASSIGN COLOUR TO LINKED CHANNEL",
            0xF6: "START AUTO CALIBRATION",
            0xF7: "QUERY GEAR FEATURES/STATUS",
            0xF8: "QUERY COLOUR STATUS",
            0xF9: "QUERY COLOUR TYPE FEATURES",
            0xFA: "QUERY COLOUR VALUE",
            0xFB: "QUERY RGBWAF CONTROL",
            0xFC: "QUERY ASSIGNED COLOUR",
            0xFF: "QUERY EXTENDED VERSION NUMBER"
        }
        if opcode in code_dictionary:
            return code_dictionary.get(opcode)
        else:
            return F"--- CODE 0x{opcode:02X} = {opcode} UNKNOWN COLOUR GEAR COMMAND"

    def gear_switch_command(self, opcode):
        # DT 7 commands
        # iec 62386 - 208 11.3.4.1
        code_dictionary = {
            0xE0: "REFERENCE SYSTEM POWER",
            0xE1: "STORE DTR AS UP SITCH-ON THRESHOLD",
            0xE2: "STORE DTR AS UP SITCH-OFF THRESHOLD",
            0xE3: "STORE DTR AS DOWN SITCH-ON THRESHOLD",
            0xE4: "STORE DTR AS DOWN SITCH-OFF THRESHOLD",
            0xE5: "STORE DTR AS ERROR HOLD-OFF TIME",
            0xF0: "QUERY FEATURES",
            0xF1: "QUERY SWITCH STATUS",
            0xF2: "QUERY UP SWITCH-ON THRESHOLD",
            0xF3: "QUERY UP SWITCH-OFF THRESHOLD",
            0xF4: "QUERY DOWN SWITCH-ON THRESHOLD",
            0xF5: "QUERY DOWN SWITCH-OFF THRESHOLD",
            0xF6: "QUERY ERROR HOLD-OFF TIME",
            0xF7: "QUERY GEAR TYPE",
            0xF9: "QUERY REFERENCE RUNNING",
            0xFA: "QUERY REFERENCE MEASUREMENT FAILED",
            0xFF: "QUERY EXTENDED VERSION NUMBER"
        }
        if opcode in code_dictionary:
            return code_dictionary.get(opcode)
        else:
            return F"--- CODE 0x{opcode:02X} = {opcode} UNKNOWN SWITCH GEAR COMMAND"

    def gear_led_command(self, opcode):
        # DT 6 commands
        # iec 62386 - 207 11.3
        code_dictionary = {
            0xE0: "REFERENCE SYTEM POWER",
            0xE3: "SELECT DIMMING CURVE (DTR0)",
            0xE4: "SET FAST FADE TIME (DTR0)",
            0xED: "QUERY CONTROL GEAR TYPE",
            0xEE: "QUERY DIMMING CURVE",
            0xF0: "QUERY FEATURES",
            0xF1: "QUERY FAILURE STATUS",
            0xF4: "QUERY LOAD DECREASE",
            0xF5: "QUERY LOAD INCREASE",
            0xF7: "QUERY THERMAL SHUTDOWN",
            0xF8: "QUERY THERMAL OVERLOAD",
            0xF9: "QUERY REFERENCE RUNNING",
            0xFA: "QUERY MEASUREMENT FAILED",
            0xFD: "QUERY FAST FADE TIME",
            0xFE: "QERYY MIN FAST FADE TIME",
            0xFF: "QUERY EXTENDED VERSION NUMBER"
        }
        if opcode in code_dictionary:
            return code_dictionary.get(opcode)
        else:
            return F"--- CODE 0x{opcode:02X} = {opcode} UNKNOWN LED GEAR COMMAND"

    def special_command(self, address_byte, opcode_byte):
        # see iec 62386-102 11.2
        if address_byte == 0xA1:
            return "TERMINATE"
        elif address_byte == 0xA3:
            return F"DTR0 0x{opcode_byte:02X} = {opcode_byte:3} = {opcode_byte:08b}b"
        elif address_byte == 0xA5:
            if (opcode_byte >> 1) >= 0x00 and (opcode_byte >> 1) <= 0x3F and (opcode_byte & 0x01):
                return F"INITIALISE (0x{(opcode_byte >> 1):02X})"
            if opcode_byte == 0xFF:
                return "INITIALISE (unaddressed)"
            if opcode_byte == 0x00:
                return "INITIALISE (all)"
            return F"INITIALISE (none) - 0x{opcode_byte:02x}"
        elif address_byte == 0xA7:
            return "RANDOMIZE"
        elif address_byte == 0xA9:
            return "COMPARE"
        elif address_byte == 0xAB:
            return "WITHDRAW"
        elif address_byte == 0xAD:
            return "PING"
        elif address_byte == 0xB1:
            return F"SEARCHADDRH 0x{opcode_byte:02X} = {opcode_byte:3} = {opcode_byte:08b}b"
        elif address_byte == 0xB3:
            return F"SEARCHADDRM 0x{opcode_byte:02X} = {opcode_byte:3} = {opcode_byte:08b}b"
        elif address_byte == 0xB5:
            return F"SEARCHADDRL 0x{opcode_byte:02X} = {opcode_byte:3} = {opcode_byte:08b}b"
        elif address_byte == 0xB7:
            if (opcode_byte >> 1) >= 0x00 and (opcode_byte >> 1) <= 0x3F and (opcode_byte & 0x01):
                opcode_byte >>= 1
                return F"PROGRAM SHORT ADDRESS (0x{opcode_byte:02X}) = {opcode_byte}"
            return F"PROGRAM SHORT ADDRESS (none) - 0x{opcode_byte:02X}"
        elif address_byte == 0xB9:
            return F"VERIFY SHORT ADDRESS (0x{opcode_byte:02X}) = {opcode_byte}"
        elif address_byte == 0xBD:
            return "PHYSICAL SELECTION (obsolete)"
        elif address_byte == 0xBB:
            return "QUERY SHORT ADDRESS"
        elif address_byte == 0xC1:
            return F"ENABLE DEVICE TYPE {opcode_byte}"
        elif address_byte == 0xC3:
            return F"DTR1 0x{opcode_byte:02X} = {opcode_byte:3} = {opcode_byte:08b}b"
        elif address_byte == 0xC5:
            return F"DTR2 0x{opcode_byte:02X} = {opcode_byte:3} = {opcode_byte:08b}b"
        elif address_byte == 0xC7:
            return F"WRITE MEMORY LOCATION DTR1, DTR0, (0x{opcode_byte:02X}) = {opcode_byte}"
        elif address_byte == 0xC9:
            return F"WRITE MEMORY LOCATION - NO REPLY - DTR1, DTR0, (0x{opcode_byte:02X}) = {opcode_byte}"
        else:
            return F"--- CODE 0x{address_byte:02X} = {address_byte} UNKNOWN CONTROL GEAR SPECIAL COMMAND"

    def __init__(self, frame, device_type=DeviceType.NONE, address_field_width=10):
        self.address_string = ""
        self.command_string = ""
        standard_command = True

        address_byte = (frame >> 8) & 0xFF
        opcode_byte = frame & 0xFF
        if (address_byte & 0x01) == 0x00:
            standard_command = False
            self.command_string = F"DAPC {opcode_byte}"
        if (address_byte >= 0x00) and (address_byte <= 0x7F):
            short_address = address_byte >> 1
            self.address_string = F"A{short_address:02}"
        elif (address_byte >= 0x80) and (address_byte <= 0x9F):
            group_address = (address_byte >> 1) & 0x0F
            self.address_string = F"G{group_address:02}"
        elif (address_byte >= 0xA0) and (address_byte <= 0xCB):
            standard_command = False
            self.command_string = self.special_command(address_byte, opcode_byte)
        elif (address_byte >= 0xCC) and (address_byte <= 0xFB):
            standard_command = False
            self.command_string = "RESERVED"
        elif (address_byte == 0xFD) or (address_byte == 0xFC):
            self.address_string = "BC unadr."
        elif (address_byte == 0xFF) or (address_byte == 0xFE):
            self.address_string = "BC"
        if standard_command:
            self.command_string = self.gear_command(opcode_byte)
            if device_type == DeviceType.COLOUR:
                self.command_string = self.gear_colour_command(opcode_byte)
            elif device_type == DeviceType.SWITCH:
                self.command_string = self.gear_switch_command(opcode_byte)
            elif device_type == DeviceType.LED:
                self.command_string = self.gear_led_command(opcode_byte)
        self.address_string = self.address_string.ljust(address_field_width, " ")        
