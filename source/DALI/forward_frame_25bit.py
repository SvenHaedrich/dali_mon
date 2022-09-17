class DeviceClass:
    SENSOR = 4
    INPUT = 5
    SEQUENCER = 6


class ForwardFrame25Bit:

    def e_DALI_sensor_command(self, opcode):
        code_dictionary = {
            0x00: "QUERY SWITCH ADDRESS",
            0x01: "QUERY CALCULATED CHECKSUM",
            0x02: "QUERY FIRMWARE VERSION",
            0x03: "QUERY EDALI VERSION",
            0x10: "START DATA DOWNLOAD",
            0x11: "STORE DTR0 AS DATA BYTE COUNTER",
            0x12: "ENABLE DIRECT MODE",
            0x13: "DISABLE DIRECT MODE",
            0x14: "ENTER BOOTLOADER",
            0x15: "HIDE MEMORY BANKS",
            0x16: "DISCOVER HIDDEN MEMORY BANKS",
            0x20: "ENHANCED RESET",
            0x21: "ENHANCED STORE SHORT ADDRESS",
            0x26: "QUERY ACTUATOR TYPE",
            0x30: "QUERY ENHANCED RESET STATE",
            0x31: "QUERY CONTROL TYPE NUMBER",
            0x32: "QUERY VERSION NUMBER CONTROL TYPE",
            0x33: "QUERY CLASS MEMBER 1-7",
            0x34: "QUERY CLASS MEMBER 8-14",
            0x35: "QUERY MULTIPLE CLASS ADDRESS",
            0x36: "QUERY MULTIPLE CLASS",
            0x37: "QUERY MISSING ENHANCED SHORT ADDRESS",
            0x38: "QUERY ENHANCED GROUPS 0-7",
            0x39: "QUERY ENHANCED GROUPS 8-15",
            0x40: "QUERY COMMISSIONING FEATURES",
            0x41: "QUERY CHANNEL SELECTOR",
            0x42: "QUERY PARAMETER POINTER",
            0x43: "QUERY PARAMTER",
            0x44: "QUERY NUMBER OF PARAMETERS",
            0x45: "START IDENTIFICATION",
            0x46: "STOP IDENTIFICATION",
            0x47: "MASSCONTROLLER ACTIVE",
            0x50: "STORE DTR0 AS PARAMETER SELECTOR",
            0x51: "STORE DTR0 AS PARAMETER POINTER",
            0x52: "STORE DTR0 AS PARAMETER",
            0x53: "START PARAMETER DOWMLOAD",
            0x54: "STOP PARAMETER DOWNLOAD",
            0x60: "QUERY MANUAL CONTROL FEATURES",
            0x61: "QUERY EVENT FEATURES",
            0x62: "QUERY MANUAL CONTROL STATUS",
            0x63: "QUERY NUMBER OF BUTTONS",
            0x64: "QUERY TYPE OF BUTTON 1-7",
            0x65: "QUERY TYPE OF BUTTON 8-15",
            0x66: "QUERY BUTTON LOCKED",
            0x67: "QUERY BUTTON LOCKED STATUS 1-7",
            0x68: "QUERY BUTTON LOCKED STATUS 8-15",
            0x69: "QUERY BUTTON STATE 1-7",
            0x6A: "QUERY BUTTON STATE 8-15",
            0x6B: "QUERY TIME LONG PRESS",
            0x6C: "QUERY TIME CONFIG1 EVENT",
            0x6D: "QUERY TIME CONFIG2 EVENT",
            0x70: "STORE DTR AS TYPE OF BUTTON 1-7",
            0x71: "STORE DTR AS TYPE OF BUTTON 8-15",
            0x72: "LOCK UNLOCK BUTTON 1-7",
            0x73: "LOCK UNLOCK BUTTON 8-15",
            0x74: "STORE DTR0 AS TIME LONG PRESS",
            0x75: "STORE DTR0 AS TIME CONFIG1 EVENT",
            0x76: "STORE DTR0 AS TIME CONFIG2 EVENT",
            0xC8: "QUERY MOTION STATUS",
            0xD4: "SET DTR0 AS DALI SHORT ADDRESS",
            0xD5: "QUERY DALI SHORT ADDRESS",
            0xD7: "QUERY SUPPORTED SENSORS",
            0xD8: "SET DTR0 AS DALI SHORT ADDRESS MODE",
            0xD9: "QUERY DALI SHORT ADDRESS MODE",
            0xDA: "STORE DTR0 AS CONSTANT LIGHT CONTROL MODE",
            0xDB: "QUERY CONSTANT LIGHT CONTROL MODE",
            0xDC: "STORE DTR0 AS CONSTANT LIGHT REFERENCE VALUE",
            0xDD: "QUERY CONSTANT LIGHT REFERENCE VALUE",
            0xE1: "SET DTR0 AS OPERATING MODE",
            0xE2: "QUERY OPERATING MODE",
            0xE3: "SET DTR0 AS EVENT MESSAGE DESTINATION ADDRESS",
            0xE4: "QUERY EVENT MESSAGE DESTINATION ADDRESS",
            0xF0: "ACTIVATE CUSTOM SCENE BEHAVIOUR",
            0xFA: "SET PRESET CONFIGURATION",
            0xFB: "QUERY CONFIGURATION BYTE"
        }
        if opcode in code_dictionary:
            return code_dictionary.get(opcode)
        else:
            return F"--- CODE 0x{opcode:02X} = {opcode} UNKNOWN eDALI SENSOR COMMAND"

    def e_DALI_input_command(self, opcode):
        code_dictionary = {
            0x00: "QUERY SWITCH ADDRESS",
            0x01: "QUERY CALCULATED CHECKSUM",
            0x02: "QUERY FIRMWARE VERSION",
            0x03: "QUERY EDALI VERSION",
            0x10: "START DATA DOWNLOAD",
            0x11: "STORE DTR0 AS DATA BYTE COUNTER",
            0x12: "ENABLE DIRECT MODE",
            0x13: "DISABLE DIRECT MODE",
            0x14: "ENTER BOOTLOADER",
            0x15: "HIDE MEMORY BANKS",
            0x16: "DISCOVER HIDDEN MEMORY BANKS",
            0x20: "ENHANCED RESET",
            0x21: "ENHANCED STORE SHORT ADDRESS",
            0x26: "QUERY ACTUATOR TYPE",
            0x30: "QUERY ENHANCED RESET STATE",
            0x31: "QUERY CONTROL TYPE NUMBER",
            0x32: "QUERY VERSION NUMBER CONTROL TYPE",
            0x33: "QUERY CLASS MEMBER 1-7",
            0x34: "QUERY CLASS MEMBER 8-14",
            0x35: "QUERY MULTIPLE CLASS ADDRESS",
            0x36: "QUERY MULTIPLE CLASS",
            0x37: "QUERY MISSING ENHANCED SHORT ADDRESS",
            0x38: "QUERY ENHANCED GROUPS 0-7",
            0x39: "QUERY ENHANCED GROUPS 8-15",
            0x40: "QUERY COMMISSIONING FEATURES",
            0x41: "QUERY CHANNEL SELECTOR",
            0x42: "QUERY PARAMETER POINTER",
            0x43: "QUERY PARAMTER",
            0x44: "QUERY NUMBER OF PARAMETERS",
            0x45: "START IDENTIFICATION",
            0x46: "STOP IDENTIFICATION",
            0x47: "MASSCONTROLLER ACTIVE",
            0x50: "STORE DTR0 AS PARAMETER SELECTOR",
            0x51: "STORE DTR0 AS PARAMETER POINTER",
            0x52: "STORE DTR0 AS PARAMETER",
            0x53: "START PARAMETER DOWMLOAD",
            0x54: "STOP PARAMETER DOWNLOAD",
            0x60: "QUERY MANUAL CONTROL FEATURES",
            0x61: "QUERY EVENT FEATURES",
            0x62: "QUERY MANUAL CONTROL STATUS",
            0x65: "MOTION SENSOR OFF-STATE",
            0x66: "MOTION SENSOR ON-STATE",
            0x69: "MOTION SENSOR MIN-STATE",
            0xB4: "EVENT MESSAGE BUTTON SHORT PRESS",
            0xB5: "EVENT MESSAGE BUTTON LONG PRESS",
            0xB6: "EVENT MESSAGE BUTTON RELEASED",
            0xB7: "EVENT MESSAGE BUTTON NEXT SHORT PRESS",
            0xC8: "QUERY MOTION STATUS",
            0xCD: "QUERY LIGHT LEVEL LOW",
            0xCE: "QUERY LIGHT LEVEL HIGH",
            0xD2: "QUERY TEMPERATURE",
            0xD4: "SET DTR0 AS DALI SHORT ADDRESS",
            0xD5: "QUERY DALI SHORT ADDRESS",
            0xD7: "QUERY SUPPORTED SENSORS",
            0xD8: "SET DTR0 AS DALI SHORT ADDRESS MODE",
            0xD9: "QUERY DALI SHORT ADDRESS MODE",
            0xDA: "STORE DTR0 AS CONSTANT LIGHT CONTROL MODE",
            0xDB: "QUERY CONSTANT LIGHT CONTROL MODE",
            0xDC: "STORE DTR0 AS CONSTANT LIGHT REFERENCE VALUE",
            0xDD: "QUERY CONSTANT LIGHT REFERENCE VALUE",
            0xE1: "SET DTR0 AS OPERATING MODE",
            0xE2: "QUERY OPERATING MODE",
            0xE3: "SET DTR0 AS EVENT MESSAGE DESTINATION ADDRESS",
            0xE4: "QUERY EVENT MESSAGE DESTINATION ADDRESS",
            0xF0: "ACTIVATE CUSTOM SCENE BEHAVIOUR",
            0xFA: "SET PRESET CONFIGURATION",
            0xFB: "QUERY CONFIGURATION BYTE"
        }
        if opcode in code_dictionary:
            return code_dictionary.get(opcode)
        else:
            return F"--- CODE 0x{opcode:02X} = {opcode} UNKNOWN eDALI INPUT COMMAND"

    def e_DALI_command(self, device_class, opcode):
        if device_class == DeviceClass.SENSOR:
            return self.e_DALI_sensor_command(opcode)
        elif device_class == DeviceClass.INPUT:
            return self.e_DALI_input_command(opcode)
        else:
            return F"--- CLASS {device_class} NOT IMPLEMENTED"

    def __init__(self, frame, address_field_width=10):
        self.address_string = "         "
        self.command_string = ""

        class_byte = (frame >> 17) & 0xF
        address_byte = (frame >> 9) & 0xFF
        opcode_byte = frame & 0xFF

        # ---- special broadcast commands
        if address_byte == 0xA1:
            self.address_string = F"C{class_byte:1d}".ljust(address_field_width)
            self.command_string = F"QUERY CONTROL TYPE (0x{opcode_byte:02X}) = {opcode_byte}"
            return
        if address_byte == 0xA3:
            self.address_string = F"C{class_byte:1d}".ljust(address_field_width)
            self.command_string = F"QUERY CONTROL CLASS (0x{(opcode_byte & 0xf):1X}) = {(opcode_byte & 0xf)}"
            return
        if address_byte == 0xA5:
            if opcode_byte == 0:
                self.address_string = F"C{class_byte:1d}".ljust(address_field_width)
                self.command_string = "ENHANCED INITIALISE (ALL)"
            elif opcode_byte == 0xFF:
                self.address_string = F"C{class_byte:1d}".ljust(address_field_width)
                self.command_string = "ENHANCED INITIALISE (UNADDRESSED)"
            else:
                self.address_string = F"C{class_byte:1d} E{((opcode_byte >> 1) & 0x3F):02d}   "
                self.command_string = "ENHANCED INITIALISE"
            return
        # ---- other commands
        if address_byte & 0x80:
            if address_byte == 0xff:
                self.address_string = F"C{class_byte:1d} BC".ljust(address_field_width)
            elif address_byte == 0xfd:
                self.address_string = F"C{class_byte:1d} BC una".ljust(address_field_width)
            else:
                self.address_string = F"C{class_byte:1d}  G{((address_byte >> 1) & 0x3F):02d}".ljust(address_field_width)
        else:
            self.address_string = F"C{class_byte:1d}  E{((address_byte >> 1) & 0x3F):02d}".ljust(address_field_width)
        self.command_string = self.e_DALI_command(class_byte, opcode_byte)
