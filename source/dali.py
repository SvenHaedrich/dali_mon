class DALIAddressing:
    SHORT = 'short addressing'
    GROUP = 'group addressing'
    BROADCAST_UNADDRESSED = 'broadcast unaddressed'
    BROADCAST = 'broadcast'
    SPECIAL_COMMAND = 'special command'
    EVENT_DEVICE = 'event device'
    EVENT_DEVICE_INSTANCE = 'event device instance'
    EVENT_DEVICE_GROUP = 'event device group'
    EVENT_INSTANCE = 'event instance'
    EVENT_INSTANCE_GROUP = 'event instance group'
    RESERVED = 'reserved'
    INVALID = 'invalid'


class DeviceTypes:
    NONE = 0
    SWITCH = 7
    COLOUR = 8


class DeviceClasses:
    SENSOR = 4
    INPUT = 5


class ForwardFrame16Bit:

    def gear_command(self, opcode):
        # see iec 62386-102 11.2
        code_dictionary = {
            0x00: 'OFF',
            0x01: 'UP',
            0x02: 'DOWN',
            0x03: 'STEP UP',
            0x04: 'STEP DOWN',
            0x05: 'RECALL MAX LEVEL',
            0x06: 'RECALL MIN LEVEL',
            0x07: 'STEP DOWN AND OFF',
            0x08: 'ON AND STEP UP',
            0x09: 'ENABLE DAPC SEQUENCE',
            0x0A: 'GO TO LAST ACTIVE LEVEL',
            0x10: 'GO TO SCENE 0',
            0x11: 'GO TO SCENE 1',
            0x12: 'GO TO SCENE 2',
            0x13: 'GO TO SCENE 3',
            0x14: 'GO TO SCENE 4',
            0x15: 'GO TO SCENE 5',
            0x16: 'GO TO SCENE 6',
            0x17: 'GO TO SCENE 7',
            0x18: 'GO TO SCENE 8',
            0x19: 'GO TO SCENE 9',
            0x1a: 'GO TO SCENE 10',
            0x1b: 'GO TO SCENE 11',
            0x1c: 'GO TO SCENE 12',
            0x1d: 'GO TO SCENE 13',
            0x1e: 'GO TO SCENE 14',
            0x1f: 'GO TO SCENE 15',
            0x20: 'RESET',
            0x21: 'STORE ACTUAL LEVEL IN DTR0',
            0x22: 'SAVE PERSISTENT VARIABLES',
            0x23: 'SET OPERATING MODE (DTR0)',
            0x24: 'RESET MEMORY BANK (DTR0)',
            0x25: 'IDENTIFY DEVICE',
            0x2A: 'SET MAX LEVEL (DTR0)',
            0x2B: 'SET MIN LEVEL (DTR0)',
            0x2C: 'SET SYSTEM FAILURE LEVEL (DTR0)',
            0x2D: 'SET SYSTEM POWER ON LEVEL (DTR0)',
            0x2E: 'SET FADE TIME (DTR0)',
            0x2F: 'SET FADE RATE (DTR0)',
            0x30: 'SET EXTENDED FADE TIME (DTR0)',
            0x40: 'SET SCENE (DTR0) 0',
            0x41: 'SET SCENE (DTR0) 1',
            0x42: 'SET SCENE (DTR0) 2',
            0x43: 'SET SCENE (DTR0) 3',
            0x44: 'SET SCENE (DTR0) 4',
            0x45: 'SET SCENE (DTR0) 5',
            0x46: 'SET SCENE (DTR0) 6',
            0x47: 'SET SCENE (DTR0) 7',
            0x48: 'SET SCENE (DTR0) 8',
            0x49: 'SET SCENE (DTR0) 9',
            0x4A: 'SET SCENE (DTR0) 10',
            0x4B: 'SET SCENE (DTR0) 11',
            0x4C: 'SET SCENE (DTR0) 12',
            0x4D: 'SET SCENE (DTR0) 13',
            0x4E: 'SET SCENE (DTR0) 14',
            0x4F: 'SET SCENE (DTR0) 15',
            0x50: 'REMOVE FROM SCENE 0',
            0x51: 'REMOVE FROM SCENE 1',
            0x52: 'REMOVE FROM SCENE 2',
            0x53: 'REMOVE FROM SCENE 3',
            0x54: 'REMOVE FROM SCENE 4',
            0x55: 'REMOVE FROM SCENE 5',
            0x56: 'REMOVE FROM SCENE 6',
            0x57: 'REMOVE FROM SCENE 7',
            0x58: 'REMOVE FROM SCENE 8',
            0x59: 'REMOVE FROM SCENE 9',
            0x5A: 'REMOVE FROM SCENE 10',
            0x5B: 'REMOVE FROM SCENE 11',
            0x5C: 'REMOVE FROM SCENE 12',
            0x5D: 'REMOVE FROM SCENE 13',
            0x5E: 'REMOVE FROM SCENE 14',
            0x5F: 'REMOVE FROM SCENE 15',
            0x60: 'ADD TO GROUP 0',
            0x61: 'ADD TO GROUP 1',
            0x62: 'ADD TO GROUP 2',
            0x63: 'ADD TO GROUP 3',
            0x64: 'ADD TO GROUP 4',
            0x65: 'ADD TO GROUP 5',
            0x66: 'ADD TO GROUP 6',
            0x67: 'ADD TO GROUP 7',
            0x68: 'ADD TO GROUP 8',
            0x69: 'ADD TO GROUP 9',
            0x6A: 'ADD TO GROUP 10',
            0x6B: 'ADD TO GROUP 11',
            0x6C: 'ADD TO GROUP 12',
            0x6D: 'ADD TO GROUP 13',
            0x6E: 'ADD TO GROUP 14',
            0x6F: 'ADD TO GROUP 15',
            0x70: 'REMOVE FROM GROUP 0',
            0x71: 'REMOVE FROM GROUP 1',
            0x72: 'REMOVE FROM GROUP 2',
            0x73: 'REMOVE FROM GROUP 3',
            0x74: 'REMOVE FROM GROUP 4',
            0x75: 'REMOVE FROM GROUP 5',
            0x76: 'REMOVE FROM GROUP 6',
            0x77: 'REMOVE FROM GROUP 7',
            0x78: 'REMOVE FROM GROUP 8',
            0x79: 'REMOVE FROM GROUP 9',
            0x7A: 'REMOVE FROM GROUP 10',
            0x7B: 'REMOVE FROM GROUP 11',
            0x7C: 'REMOVE FROM GROUP 12',
            0x7D: 'REMOVE FROM GROUP 13',
            0x7E: 'REMOVE FROM GROUP 14',
            0x7F: 'REMOVE FROM GROUP 15',
            0x80: 'SET SHORT ADDRESS (DTR0)',
            0x81: 'ENABLE WRITE MEMORY',
            0x90: 'QUERY STATUS',
            0x91: 'QUERY CONTROL GEAR PRESENT',
            0x92: 'QUERY LAMP FAILURE',
            0x93: 'QUERY LAMP POWER ON',
            0x94: 'QUERY LIMIT ERROR',
            0x95: 'QUERY RESET STATE',
            0x96: 'QUERY MISSING SHORT ADDRESS',
            0x97: 'QUERY VERSION NUMBER',
            0x98: 'QUERY CONTENT DTR0',
            0x99: 'QUERY DEVICE TYPE',
            0x9A: 'QUERY PHYSICAL MINIMUM',
            0x9B: 'QUERY POWER FAILURE',
            0x9C: 'QUERY CONTENT DTR1',
            0x9D: 'QUERY CONTENT DTR2',
            0x9E: 'QUERY OPERATING MODE',
            0x9F: 'QUERY LIGHT SOURCE TYPE',
            0xA0: 'QUERY ACTUAL LEVEL',
            0xA1: 'QUERY MAX LEVEL',
            0XA2: 'QUERY MIN LEVEL',
            0xA3: 'QUERY POWER ON LEVEL',
            0xA4: 'QUERY SYSTEM FAILURE LEVEL',
            0xA5: 'QUERY FADE TIME / FADE RATE',
            0xA6: 'QUERY MANUFACTURER SPECIFIC MODE',
            0xA7: 'QUERY NEXT DEVICE TYPE',
            0xA8: 'QUERY EXTENDED FADE TIME',
            0xAA: 'QUERY CONTROL GEAR FAILURE',
            0xB0: 'QUERY SCENE LEVEL 0',
            0xB1: 'QUERY SCENE LEVEL 1',
            0xB2: 'QUERY SCENE LEVEL 2',
            0xB3: 'QUERY SCENE LEVEL 3',
            0xB4: 'QUERY SCENE LEVEL 4',
            0xB5: 'QUERY SCENE LEVEL 5',
            0xB6: 'QUERY SCENE LEVEL 6',
            0xB7: 'QUERY SCENE LEVEL 7',
            0xB8: 'QUERY SCENE LEVEL 8',
            0xB9: 'QUERY SCENE LEVEL 9',
            0xBA: 'QUERY SCENE LEVEL 10',
            0xBB: 'QUERY SCENE LEVEL 11',
            0xBC: 'QUERY SCENE LEVEL 12',
            0xBD: 'QUERY SCENE LEVEL 13',
            0xBE: 'QUERY SCENE LEVEL 14',
            0xBF: 'QUERY SCENE LEVEL 15',
            0xC0: 'QUERY GROUPS 0-7',
            0xC1: 'QUERY GROUPS 8-15',
            0xC2: 'QUERY RANDOM ADDRESS (H)',
            0xC3: 'QUERY RANDOM ADDRESS (M)',
            0xC4: 'QUERY RANDOM ADDRESS (L)',
            0xC5: 'READ MEMORY LOCATION (DTR1,DTR0)',
            0xFF: 'QUERY EXTENDED VERSION NUMBER'
        }
        if opcode in code_dictionary:
            return code_dictionary.get(opcode)
        else:
            return 'code 0x{:02x} (= {}) undefined control gear command'.format(opcode, opcode)

    def gear_colour_command(self, opcode):
        code_dictionary = {
            0xE0: 'SET TEMPORARY X-COORDINATE',
            0xE1: 'SET TEMPORARY Y-COORDINATE',
            0xE2: 'ACTIVATE',
            0xE3: 'X-COORDINATE STEP UP',
            0XE4: 'X-COORDINATE STEP DOWN',
            0xE5: 'Y-COORDINATE STEP UP',
            0xE6: 'Y-COORDINATE STEP DOWN',
            0xE7: 'SET TEMPORARY COLOUR TEMPERATURE TC',
            0xE8: 'COLOUR TEMPERATURE TC STEP COOLER',
            0xE9: 'COLOUR TEMPERTAURE TC STEP WARMER',
            0xEA: 'SET TEMPORARY PRIMARY N DIMLEVEL',
            0xEB: 'SET TEMPORARY RGB DIMLEVEL',
            0xEC: 'SET TEMPORARY WAF DIMLEVEL',
            0xED: 'SET TEMPORARY RGBWAF CONTROL',
            0xEE: 'COPY REPORT TO TEMPORARY',
            0xEF: 'reserved for future needs',
            0xF0: 'STORE TY PRIMARY N',
            0xF1: 'STORE XY-COORDINATE PRIMARY N',
            0xF2: 'STORE COLOUR TEMPERATURE TC LIMIT',
            0xF3: 'STORE GEAR FEATURE/STATUS',
            0xF4: 'reserved for future needs',
            0xF5: 'ASSIGN COLOUR TO LINKED CHANNEL',
            0xF6: 'START AUTO CALIBRATION',
            0xF7: 'QUERY GEAR FEATURES/STATUS',
            0xF8: 'QUERY COLOUR STATUS',
            0xF9: 'QUERY COLOUR TYPE FEATURES',
            0xFA: 'QUERY COLOUR VALUE',
            0xFB: 'QUERY RGBWAF CONTROL',
            0xFC: 'QUERY ASSIGNED COLOUR',
            0xFD: 'reserved for future needs',
            0xFE: 'reserved for future needs',
            0xFF: 'QUERY EXTENDED VERSION NUMBER'
        }
        if not opcode in code_dictionary:
            return '---'
        else:
            return code_dictionary.get(opcode)

    def special_command(self, address_byte, opcode_byte, device_type):
        # see iec 62386-102 11.2
        if address_byte == 0xA1:
            return 'TERMINATE'
        elif address_byte == 0xA3:
            return 'DTR0 0x{:02X} = {:3} = {:08b}b'.format(opcode_byte, opcode_byte, opcode_byte)
        elif address_byte == 0xA5:
            if (opcode_byte >> 1) >= 0x00 and (opcode_byte >> 1) <= 0x3F and (opcode_byte & 0x01):
                return 'INITIALISE (0x{:02X})'.format(opcode_byte >> 1)
            if opcode_byte == 0xFF:
                return 'INITIALISE (unaddressed)'
            if opcode_byte == 0x00:
                return 'INITIALISE (all)'
            return 'INITIALISE (none) - 0x{:02x}'.format(opcode_byte)
        elif address_byte == 0xA7:
            return 'RANDOMIZE'
        elif address_byte == 0xA9:
            return 'COMPARE'
        elif address_byte == 0xAB:
            return 'WITHDRAW'
        elif address_byte == 0xAD:
            return 'PING'
        elif address_byte == 0xB1:
            return 'SEARCHADDRH 0x{:02X} = {:3} = {:08b}b'.format(opcode_byte, opcode_byte, opcode_byte)
        elif address_byte == 0xB3:
            return 'SEARCHADDRM 0x{:02X} = {:3} = {:08b}b'.format(opcode_byte, opcode_byte, opcode_byte)
        elif address_byte == 0xB5:
            return 'SEARCHADDRL 0x{:02X} = {:3} = {:08b}b'.format(opcode_byte, opcode_byte, opcode_byte)
        elif address_byte == 0xB7:
            if (opcode_byte >> 1) >= 0x00 and (opcode_byte >> 1) <= 0x3F and (opcode_byte & 0x01):
                return 'PROGRAM SHORT ADDRESS (0x{:02X}) = {}'.format(opcode_byte >> 1, opcode_byte >> 1)
            return 'PROGRAM SHORT ADDRESS (none) - 0x{:02X}'.format(opcode_byte)
        elif address_byte == 0xB9:
            return 'VERIFY SHORT ADDRESS (0x{:02X}) = {}'.format(opcode_byte, opcode_byte)
        elif address_byte == 0xBD:
            return 'PHYSICAL SELECTION (obsolete)'
        elif address_byte == 0xBB:
            return 'QUERY SHORT ADDRESS'
        elif address_byte == 0xC1:
            return 'ENABLE DEVICE TYPE {}'.format(opcode_byte)
        elif address_byte == 0xC3:
            return 'DTR1 0x{:02X} = {:3} = {:08b}b'.format(opcode_byte, opcode_byte, opcode_byte)
        elif address_byte == 0xC5:
            return 'DTR2 0x{:02X} = {:3} = {:08b}b'.format(opcode_byte, opcode_byte, opcode_byte)
        elif address_byte == 0xC7:
            return 'WRITE MEMORY LOCATION DTR1, DTR0, (0x{:02X}) = {}'.format(opcode_byte, opcode_byte)
        elif address_byte == 0xC9:
            return 'WRITE MEMORY LOCATION - NO REPLY - DTR1, DTR0, (0x{:02X}) = {}'.format(opcode_byte, opcode_byte)
        else:
            return 'code 0x{:0x} (= {}) undefined control gear special command'.format(address_byte, address_byte)

    def __init__(self, frame, device_type=DeviceTypes.NONE):
        self.short_address = DALIAddressing.INVALID
        self.group_address = DALIAddressing.INVALID
        self.adressing = DALIAddressing.INVALID
        self.address_string = ''
        self.command_string = ''
        self.dapc = False

        address_byte = (frame >> 8) & 0xFF
        opcode_byte = frame & 0xFF
        if (address_byte & 0x01) == 0x00:
            self.dapc = True
            self.command_string = 'DAPC {}'.format(opcode_byte)
        if (address_byte >= 0x00) and (address_byte <= 0x7F):
            self.addressing = DALIAddressing.SHORT
            short_address = address_byte >> 1
            self.address_string = 'A{:02}      '.format(short_address)
        elif (address_byte >= 0x80) and (address_byte <= 0x9F):
            self.addressing = DALIAddressing.GROUP
            group_address = (address_byte >> 1) & 0x0F
            self.address_string = 'G{:02}      '.format(group_address)
        elif (address_byte >= 0xA0) and (address_byte <= 0xCB):
            self.addressing = DALIAddressing.SPECIAL_COMMAND
            self.command_string = '         ' + \
                self.special_command(address_byte, opcode_byte, device_type)
        elif (address_byte >= 0xCC) and (address_byte <= 0xFB):
            self.addressing = DALIAddressing.RESERVED
        elif (address_byte == 0xFD) or (address_byte == 0xFC):
            self.addressing = DALIAddressing.BROADCAST_UNADDRESSED
            self.address_string = 'BC unadr.'
        elif (address_byte == 0xFF) or (address_byte == 0xFE):
            self.addressing = DALIAddressing.BROADCAST
            self.address_string = 'BC       '
        if (not self.dapc) and (self.addressing != DALIAddressing.SPECIAL_COMMAND):
            self.command_string = self.gear_command(opcode_byte)
            if device_type == DeviceTypes.COLOUR:
                self.command_string = self.gear_colour_command(opcode_byte)


class ForwardFrame24Bit:

    def device_command(self, opcode):
        # see iec 62386-102 11.2
        code_dictionary = {
            0x00: 'IDENTIFY DEVICE',
            0x01: 'RESET POWER CYCLE SEEN',
            0x10: 'RESET',
            0x11: 'RESET MEMORY BANK (DTR0)',
            0x14: 'SET SHORT ADDRESS (DTR0)',
            0x15: 'ENABLE WRITE MEMORY',
            0x16: 'ENABLE APPLICATION CONTROLLER',
            0x17: 'DISABLE APPLICATION CONTROLLER',
            0x18: 'SET OPERATING MODE (DTR0)',
            0x19: 'ADD TO DEVICE GROUPS 0-15 (DTR2:DTR1)',
            0x1A: 'ADD TO DEVICE GROUPS 16-31 (DTR2:DTR1)',
            0x1B: 'REMOVE FROM DEVICE GROUPS 0-15 (DTR2:DTR1)',
            0x1C: 'REMOVE FROM DEVICE GROUPS 16-31 (DTR2:DTR1)',
            0x1D: 'START QUIESCENT MODE',
            0x1E: 'STOP QUIESCENT MODE',
            0x1F: 'ENABLE POWER CYCLE NOTIFICATION',
            0x20: 'DISABLE POWER CYCLE NOTIFICATION',
            0x21: 'SAVE PERSISTENT VARIABLES',
            0x30: 'QUERY DEVICE STATUS',
            0x31: 'QUERY APPLICTAION CONTROLLER ERROR',
            0x32: 'QUERY INPUT DEVICE ERROR',
            0x33: 'QUERY MISSING SHORT ADDRESS',
            0x34: 'QUERY VERSION NUMBER',
            0x35: 'QUERY NUMBER OF INSTANCES',
            0x36: 'QUERY CONTENT DTR0',
            0x37: 'QUERY CONTENT DTR1',
            0x38: 'QUERY CONTENT DTR2',
            0x39: 'QUERY RANDOM ADDRESS (H)',
            0x3A: 'QUERY RANDOM ADDRESS (M)',
            0x3B: 'QUERY RANDOM ADDRESS (L)',
            0x3C: 'READ MEMORY LOCATION (DTR1,DTR0)',
            0x3D: 'QUERY APPLICATION CONTROL ENABLED',
            0x3E: 'QUERY OPERATING MODE',
            0x3F: 'QUERY MANUFACTURER SPECIFIC MODE',
            0x40: 'QUERY QUIESCENT MODE',
            0x41: 'QUERY DEVICE GROUPS 0-7',
            0x42: 'QUERY DEVICE GROUPS 8-15',
            0x43: 'QUERY DEVICE GROUPS 16-23',
            0x44: 'QUERY DEVICE GROUPS 24-41',
            0x45: 'QUERY POWER CYCLE NOTIFICATION',
            0x46: 'QUERY DEVICE CAPABILITIES',
            0x47: 'QUERY EXTENDED VERSION NUMBER (DTR0)',
            0x48: 'QUERY RESET STATE',
            0x61: 'SET EVENT PRIORITY (DTR0)',
            0x62: 'ENABLE INSTANCE',
            0x63: 'DISABLE INSTANCE',
            0x64: 'SET PRIMARY INSTANCE GROUP (DTR0)',
            0x65: 'SET INSTANCE GROUP 1 (DTR0)',
            0x66: 'SET INSTANCE GROUP 2 (DTR0)',
            0x67: 'SET EVENT SCHEME (DTR0)',
            0x68: 'SET EVENT FILTER (DTR2, DTR1, DTR0)',
            0x80: 'QUERY INSTANCE TYPE',
            0x81: 'QUERY RESOLUTION',
            0x82: 'QUERY INSTANCE ERROR',
            0x83: 'QUERY INSTANCE STATUS',
            0x84: 'QUERY EVENT PRIORITY',
            0x86: 'QUERY INSTANCE ENABLED',
            0x88: 'QUERY PRIMARY INSTANCE GROUP',
            0x89: 'QUERY INSTANCE GROUP 1',
            0x8A: 'QUERY INSTANCE GROUP 2',
            0x8B: 'QUERY EVENT SCHEME',
            0x8C: 'QUERY INPUT VALUE',
            0x8D: 'QUERY INPUT VALUE LATCH',
            0x8E: 'QUERY FEATURE TYPE',
            0x8F: 'QUERY NEXT FEATURE TYPE',
            0x90: 'QUERY EVENT FILTER 0-7',
            0x91: 'QUERY EVENT FILTER 8-15',
            0x92: 'QUERY EVENT FILTER 16-23'
        }
        if not opcode in code_dictionary:
            return 'code 0x{:02x} (={} dec) undefined control device command'.format(opcode, opcode)
        else:
            return code_dictionary.get(opcode)

    def device_special_command(self, address_byte, instance_byte, opcode_byte):
        # see iec 62386-103 table 22
        if address_byte == 0xc1:
            if instance_byte == 0x00:
                return 'TERMINATE'
            elif instance_byte == 0x01:
                return 'INITIALISE (0x{:02X})'.format(opcode_byte)
            elif instance_byte == 0x02:
                return 'RANDOMISE'
            elif instance_byte == 0x03:
                return 'COMPARE'
            elif instance_byte == 0x04:
                return 'WITHDRAW'
            elif instance_byte == 0x05:
                return 'SEARCHADDRH (0x{:02X}) = {}'.format(opcode_byte, opcode_byte)
            elif instance_byte == 0x06:
                return 'SEARCHADDRM (0x{:02X}) = {}'.format(opcode_byte, opcode_byte)
            elif instance_byte == 0x07:
                return 'SEARCHADDRL (0x{:02X}) = {}'.format(opcode_byte, opcode_byte)
            elif instance_byte == 0x08:
                return 'PROGRAM SHORT ADDRESS (0x{:02X}) = {}'.format(opcode_byte, opcode_byte)
            elif instance_byte == 0x09:
                return 'VERIFY SHORT ADDRESS (0x{:02X}) = {}'.format(opcode_byte, opcode_byte)
            elif instance_byte == 0x0a:
                return 'QUERY SHORT ADDRESS'
            elif instance_byte == 0x20:
                return 'WRITE MEMORY LOCATION DTR1, DTR0, (0x{:02X}) = {}'.format(opcode_byte, opcode_byte)
            elif instance_byte == 0x21:
                return 'WRITE MEMORY LOCATION - NO REPLY - DTR1, DTR0, (0x{:02X}) = {}'.format(opcode_byte, opcode_byte)
            elif instance_byte == 0x30:
                return 'DTR0 0x{:02X} = {:3} = {:08b}'.format(opcode_byte, opcode_byte, opcode_byte)
            elif instance_byte == 0x31:
                return 'DTR1 0x{:02X} = {:3} = {:08b}'.format(opcode_byte, opcode_byte, opcode_byte)
            elif instance_byte == 0x32:
                return 'DTR2 0x{:02X} = {:3} = {:08b}'.format(opcode_byte, opcode_byte, opcode_byte)
            elif instance_byte == 0x33:
                return 'SEND TESTFRAME (0x{:02X}) = {}'.format(opcode_byte, opcode_byte)
        if address_byte == 0xc5:
            return 'DIRECT WRITE MEMORY (DTR0,0x{:02X}) : 0x{:02X}'.format(instance_byte, opcode_byte)
        if address_byte == 0xc7:
            return 'DTR1:DTR0 (0x{:02X},0x{:02X})'.format(instance_byte, opcode_byte)
        if address_byte == 0xc9:
            return 'DTR2:DTR1 (0x{:02X},0x{:02X})'.format(instance_byte, opcode_byte)

    def get_event_source_type(self, frame):
        if (frame & (1 << 23)):
            if (frame & (1 << 22)):
                return DALIAddressing.EVENT_INSTANCE_GROUP
            else:
                if (frame & (1 << 15)):
                    return DALIAddressing.EVENT_INSTANCE
                else:
                    return DALIAddressing.EVENT_DEVICE_GROUP
        else:
            if (frame & (1 << 15)):
                return DALIAddressing.EVENT_DEVICE_INSTANCE
            else:
                return DALIAddressing.EVENT_DEVICE
        return DALIAddressing.INVALID

    def built_event_source_string(self, event_type, frame):
        if (event_type == DALIAddressing.EVENT_DEVICE):
            short_address = (frame >> 17) & 0x3F
            instance_type = (frame >> 10) & 0x1F
            return 'A{:02X},T{:02X}  '.format(short_address, instance_type)
        elif (event_type == DALIAddressing.EVENT_DEVICE_INSTANCE):
            short_address = (frame >> 17) & 0x3F
            instance_number = (frame >> 10) & 0x1F
            return 'A{:02X},I{:02X}  '.format(short_address, instance_number)
        elif (event_type == DALIAddressing.EVENT_DEVICE_GROUP):
            device_group = (frame >> 17) & 0x1F
            instance_type = (frame >> 10) & 0x1F
            return 'G{:02X},T{:02X}  '.format(device_group, instance_type)
        elif (event_type == DALIAddressing.EVENT_INSTANCE):
            instance_type = (frame >> 17) & 0x1F
            instance_number = (low_byte >> 2) & 0x1F
            return 'T{:02X},I{:02X}  '.fromat(instance_type, instance_number)
        elif (event_type == DALIAddressing.EVENT_INSTANCE_GROUP):
            device_group = (frame >> 17) & 0x1F
            instance_type = (frame >> 10) & 0x1F
            return 'IG{:02X},T{:02X} '.format(device_group, instance_type)
        else:
            return 'invalid  '

    def __init__(self, frame):
        self.adressing = DALIAddressing.INVALID
        self.address_string = ''
        self.command_string = ''

        address_byte = (frame >> 16) & 0xFF
        instance_byte = (frame >> 8) & 0xFF
        opcode_byte = frame & 0xFF

        if address_byte == 0xFE:
            if (opcode_byte & 0x40) == 0x40:
                self.address_string = 'A{:02}      '.format(opcode_byte & 0x3f)
            else:
                self.address_string = 'BC       '
            self.command_string = 'POWER CYCLE EVENT'
            return
        if not (address_byte & 0x01):
            self.addressing = self.get_event_source_type(frame)
            self.address_string = self.built_event_source_string(
                self.addressing, frame)
            self.command_string = 'EVENT DATA 0x{:03X} = {} = {:012b}b'.format(
                (frame & 0x3FF), (frame & 0x3FF), (frame & 0x3FF))
            return
        if (address_byte >= 0x00) and (address_byte <= 0x7F):
            self.addressing = DALIAddressing.SHORT
            short_address = address_byte >> 1
            self.address_string = 'A{:02}      '.format(short_address)
            self.command_string = self.device_command(opcode_byte)
            return
        if (address_byte >= 0x80) and (address_byte <= 0xBF):
            self.addressing = DALIAddressing.GROUP
            group_address = ((address_byte >> 1) & 0x0F)
            self.address_string = 'G{:02}      '.format(group_address)
            self.command_string = self.device_command(opcode_byte)
            return
        if address_byte == 0xFD:
            self.addressing = DALIAddressing.BROADCAST_UNADDRESSED
            self.address_string = 'BC unadr.'
            self.command_string = self.device_command(opcode_byte)
        elif address_byte == 0xFF:
            self.addressing = DALIAddressing.BROADCAST
            self.address_string = 'BC       '
            self.command_string = self.device_command(opcode_byte)
        elif (address_byte >= 0xC1) and (address_byte <= 0xDF):
            self.addressing = DALIAddressing.SPECIAL_COMMAND
            self.command_string = '         ' + \
                self.device_special_command(
                    address_byte, instance_byte, opcode_byte)
        elif (address_byte >= 0xE1) and (address_byte <= 0xEF):
            self.addressing = DALIAddressing.RESERVED
        elif (address_byte >= 0xF1) and (address_byte <= 0xF7):
            self.addressing = DALIAddressing.RESERVED
        elif (address_byte >= 0xF8) and (address_byte <= 0xFB):
            self.addressing = DALIAddressing.RESERVED


class ForwardFrame25Bit:

    def e_DALI_sensor_command(self, opcode):
        code_dictionary = {
            0x00: 'QUERY SWITCH ADDRESS',
            0x01: 'QUERY CALCULATED CHECKSUM',
            0x02: 'QUERY FIRMWARE VERSION',
            0x03: 'QUERY EDALI VERSION',
            0x10: 'START DATA DOWNLOAD',
            0x11: 'STORE DTR0 AS DATA BYTE COUNTER',
            0x12: 'ENABLE DIRECT MODE',
            0x13: 'DISABLE DIRECT MODE',
            0x14: 'ENTER BOOTLOADER',
            0x15: 'HIDE MEMORY BANKS',
            0x16: 'DISCOVER HIDDEN MEMORY BANKS',
            0x20: 'ENHANCED RESET',
            0x21: 'ENHANCED STORE SHORT ADDRESS',
            0x26: 'QUERY ACTUATOR TYPE',
            0x30: 'QUERY ENHANCED RESET STATE',
            0x31: 'QUERY CONTROL TYPE NUMBER',
            0x32: 'QUERY VERSION NUMBER CONTROL TYPE',
            0x33: 'QUERY CLASS MEMBER 1-7',
            0x34: 'QUERY CLASS MEMBER 8-14',
            0x35: 'QUERY MULTIPLE CLASS ADDRESS',
            0x36: 'QUERY MULTIPLE CLASS',
            0x37: 'QUERY MISSING ENHANCED SHORT ADDRESS',
            0x38: 'QUERY ENHANCED GROUPS 0-7',
            0x39: 'QUERY ENHANCED GROUPS 8-15',
            0x40: 'QUERY COMMISSIONING FEATURES',
            0x41: 'QUERY CHANNEL SELECTOR',
            0x42: 'QUERY PARAMETER POINTER',
            0x43: 'QUERY PARAMTER',
            0x44: 'QUERY NUMBER OF PARAMETERS',
            0x45: 'START IDENTIFICATION',
            0x46: 'STOP IDENTIFICATION',
            0x47: 'MASSCONTROLLER ACTIVE',
            0x50: 'STORE DTR0 AS PARAMETER SELECTOR',
            0x51: 'STORE DTR0 AS PARAMETER POINTER',
            0x52: 'STORE DTR0 AS PARAMETER',
            0x53: 'START PARAMETER DOWMLOAD',
            0x54: 'STOP PARAMETER DOWNLOAD',
            0x60: 'QUERY MANUAL CONTROL FEATURES',
            0x61: 'QUERY EVENT FEATURES',
            0x62: 'QUERY MANUAL CONTROL STATUS',
            0x63: 'QUERY NUMBER OF BUTTONS',
            0x64: 'QUERY TYPE OF BUTTON 1-7',
            0x65: 'QUERY TYPE OF BUTTON 8-15',
            0x66: 'QUERY BUTTON LOCKED',
            0x67: 'QUERY BUTTON LOCKED STATUS 1-7',
            0x68: 'QUERY BUTTON LOCKED STATUS 8-15',
            0x69: 'QUERY BUTTON STATE 1-7',
            0x6A: 'QUERY BUTTON STATE 8-15',
            0x6B: 'QUERY TIME LONG PRESS',
            0x6C: 'QUERY TIME CONFIG1 EVENT',
            0x6D: 'QUERY TIME CONFIG2 EVENT',
            0x70: 'STORE DTR AS TYPE OF BUTTON 1-7',
            0x71: 'STORE DTR AS TYPE OF BUTTON 8-15',
            0x72: 'LOCK UNLOCK BUTTON 1-7',
            0x73: 'LOCK UNLOCK BUTTON 8-15',
            0x74: 'STORE DTR0 AS TIME LONG PRESS',
            0x75: 'STORE DTR0 AS TIME CONFIG1 EVENT',
            0x76: 'STORE DTR0 AS TIME CONFIG2 EVENT',
            0xC8: 'QUERY MOTION STATUS',
            0xD4: 'SET DTR0 AS DALI SHORT ADDRESS',
            0xD5: 'QUERY DALI SHORT ADDRESS',
            0xD7: 'QUERY SUPPORTED SENSORS',
            0xD8: 'SET DTR0 AS DALI SHORT ADDRESS MODE',
            0xD9: 'QUERY DALI SHORT ADDRESS MODE',
            0xDA: 'STORE DTR0 AS CONSTANT LIGHT CONTROL MODE',
            0xDB: 'QUERY CONSTANT LIGHT CONTROL MODE',
            0xDC: 'STORE DTR0 AS CONSTANT LIGHT REFERENCE VALUE',
            0xDD: 'QUERY CONSTANT LIGHT REFERENCE VALUE',
            0xE1: 'SET DTR0 AS OPERATING MODE',
            0xE2: 'QUERY OPERATING MODE',
            0xE3: 'SET DTR0 AS EVENT MESSAGE DESTINATION ADDRESS',
            0xE4: 'QUERY EVENT MESSAGE DESTINATION ADDRESS',
            0xF0: 'ACTIVATE CUSTOM SCENE BEHAVIOUR',
            0xFA: 'SET PRESET CONFIGURATION',
            0xFB: 'QUERY CONFIGURATION BYTE'
        }
        if not opcode in code_dictionary:
            return '--- UNKNOWN COMMAND SENSOR CLASS'
        else:
            return code_dictionary.get(opcode)

    def e_DALI_input_command(self, opcode):
        code_dictionary = {
            0x00: 'QUERY SWITCH ADDRESS',
            0x01: 'QUERY CALCULATED CHECKSUM',
            0x02: 'QUERY FIRMWARE VERSION',
            0x03: 'QUERY EDALI VERSION',
            0x10: 'START DATA DOWNLOAD',
            0x11: 'STORE DTR0 AS DATA BYTE COUNTER',
            0x12: 'ENABLE DIRECT MODE',
            0x13: 'DISABLE DIRECT MODE',
            0x14: 'ENTER BOOTLOADER',
            0x15: 'HIDE MEMORY BANKS',
            0x16: 'DISCOVER HIDDEN MEMORY BANKS',
            0x20: 'ENHANCED RESET',
            0x21: 'ENHANCED STORE SHORT ADDRESS',
            0x26: 'QUERY ACTUATOR TYPE',
            0x30: 'QUERY ENHANCED RESET STATE',
            0x31: 'QUERY CONTROL TYPE NUMBER',
            0x32: 'QUERY VERSION NUMBER CONTROL TYPE',
            0x33: 'QUERY CLASS MEMBER 1-7',
            0x34: 'QUERY CLASS MEMBER 8-14',
            0x35: 'QUERY MULTIPLE CLASS ADDRESS',
            0x36: 'QUERY MULTIPLE CLASS',
            0x37: 'QUERY MISSING ENHANCED SHORT ADDRESS',
            0x38: 'QUERY ENHANCED GROUPS 0-7',
            0x39: 'QUERY ENHANCED GROUPS 8-15',
            0x40: 'QUERY COMMISSIONING FEATURES',
            0x41: 'QUERY CHANNEL SELECTOR',
            0x42: 'QUERY PARAMETER POINTER',
            0x43: 'QUERY PARAMTER',
            0x44: 'QUERY NUMBER OF PARAMETERS',
            0x45: 'START IDENTIFICATION',
            0x46: 'STOP IDENTIFICATION',
            0x47: 'MASSCONTROLLER ACTIVE',
            0x50: 'STORE DTR0 AS PARAMETER SELECTOR',
            0x51: 'STORE DTR0 AS PARAMETER POINTER',
            0x52: 'STORE DTR0 AS PARAMETER',
            0x53: 'START PARAMETER DOWMLOAD',
            0x54: 'STOP PARAMETER DOWNLOAD',
            0x60: 'QUERY MANUAL CONTROL FEATURES',
            0x61: 'QUERY EVENT FEATURES',
            0x62: 'QUERY MANUAL CONTROL STATUS',
            0x65: 'MOTION SENSOR OFF-STATE',
            0x66: 'MOTION SENSOR ON-STATE',
            0x69: 'MOTION SENSOR MIN-STATE',
            0xB4: 'EVENT MESSAGE BUTTON SHORT PRESS',
            0xB5: 'EVENT MESSAGE BUTTON LONG PRESS',
            0xB6: 'EVENT MESSAGE BUTTON RELEASED',
            0xB7: 'EVENT MESSAGE BUTTON NEXT SHORT PRESS',
            0xC8: 'QUERY MOTION STATUS',
            0xCD: 'QUERY LIGHT LEVEL LOW',
            0xCE: 'QUERY LIGHT LEVEL HIGH',
            0xD2: 'QUERY TEMPERATURE',
            0xD4: 'SET DTR0 AS DALI SHORT ADDRESS',
            0xD5: 'QUERY DALI SHORT ADDRESS',
            0xD7: 'QUERY SUPPORTED SENSORS',
            0xD8: 'SET DTR0 AS DALI SHORT ADDRESS MODE',
            0xD9: 'QUERY DALI SHORT ADDRESS MODE',
            0xDA: 'STORE DTR0 AS CONSTANT LIGHT CONTROL MODE',
            0xDB: 'QUERY CONSTANT LIGHT CONTROL MODE',
            0xDC: 'STORE DTR0 AS CONSTANT LIGHT REFERENCE VALUE',
            0xDD: 'QUERY CONSTANT LIGHT REFERENCE VALUE',
            0xE1: 'SET DTR0 AS OPERATING MODE',
            0xE2: 'QUERY OPERATING MODE',
            0xE3: 'SET DTR0 AS EVENT MESSAGE DESTINATION ADDRESS',
            0xE4: 'QUERY EVENT MESSAGE DESTINATION ADDRESS',
            0xF0: 'ACTIVATE CUSTOM SCENE BEHAVIOUR',
            0xFA: 'SET PRESET CONFIGURATION',
            0xFB: 'QUERY CONFIGURATION BYTE'
        }
        if not opcode in code_dictionary:
            return '--- UNKNOWN COMMAND INPUT CLASS'
        else:
            return code_dictionary.get(opcode)

    def e_DALI_command(self, device_class, opcode):
        if device_class == DeviceClasses.SENSOR:
            return self.e_DALI_sensor_command(opcode)
        elif device_class == DeviceClasses.INPUT:
            return self.e_DALI_input_command(opcode)
        else:
            return '--- UNKNOWN CLASS'

    def __init__(self, frame):
        self.adressing = DALIAddressing.INVALID
        self.address_string = ''
        self.command_string = ''

        class_byte = (frame >> 17) & 0xF
        address_byte = (frame >> 9) & 0xFF
        opcode_byte = frame & 0xFF

        # ---- special broadcast commands
        if address_byte == 0xA1:
            self.address_string = 'C{:1d}       '.format(class_byte)
            self.command_string = 'QUERY CONTROL TYPE (0x{:02X}) = {}'.format(
                opcode_byte, opcode_byte)
            return
        if address_byte == 0xA3:
            self.address_string = 'C{:1d}       '.format(class_byte)
            self.command_string = 'QUERY CONTROL CLASS (0x{:1X}) = {}'.format(
                (opcode_byte & 0xf), (opcode_byte & 0xF))
            return
        if address_byte == 0xA5:
            if opcode_byte == 0:
                self.address_string = 'C{:1d}       '.format(class_byte)
                self.command_string = 'ENHANCED INITIALISE (ALL)'
            elif opcode_byte == 0xFF:
                self.address_string = 'C{:1d}       '.format(class_byte)
                self.command_string = 'ENHANCED INITIALISE (UNADDRESSED)'
            else:
                self.address_string = 'C{:1d} E{:02d}   '.format(
                    class_byte, ((opcode_byte >> 1) & 0x3F))
                self.command_string = 'ENHANCED INITIALISE'
            return
        # ---- other commands
        if address_byte & 0x80:
            if address_byte == 0xff:
                self.address_string = 'C{:1d} BC    '.format(class_byte)
            elif address_byte == 0xfd:
                self.address_string = 'C{:1d} BC una'.format(class_byte)
            else:
                self.address_string = 'C{:1d} G{:02d}   '.format(
                    class_byte, ((address_byte >> 1) & 0x3F))
        else:
            self.address_string = 'C{:1d} E{:02d}   '.format(
                class_byte, ((address_byte >> 1) & 0x3F))
        self.command_string = self.e_DALI_command(class_byte, opcode_byte)


class Frame:
    def __init__(self, length, frame, device_type=DeviceTypes.NONE):
        self.length = length
        self.frame = frame
        self.result = ''
        self.active = device_type

        if self.length == 16:
            address_byte = (self.frame >> 8) & 0xFF
            if address_byte == 0xC1:
                self.enable = (self.frame & 0xFF)
            else:
                self.enable = DeviceTypes.NONE
        else:
            self.enable = DeviceTypes.NONE

    def __str__(self):
        if self.length == 8:
            return '      {:02X}'.format(self.frame)
        elif self.length == 16:
            return '    {:04X}'.format(self.frame)
        elif self.length == 24:
            return '  {:06X}'.format(self.frame)
        elif self.length == 25:
            return ' {:07X}'.format(self.frame)
        else:
            return '{:08X}'.format(self.frame)

    def cmd(self):
        if self.length == 16:
            frame_type = ForwardFrame16Bit(self.frame, self.active)
            return frame_type.address_string + '   ' + frame_type.command_string
        if self.length == 24:
            frame_type = ForwardFrame24Bit(self.frame)
            return frame_type.address_string + '   ' + frame_type.command_string
        if self.length == 25:
            frame_type = ForwardFrame25Bit(self.frame)
            return frame_type.address_string + '   ' + frame_type.command_string
        if self.length == 8:
            return '            DATA 0x{:02X} = {:3} = {:08b}b'.format(self.frame, self.frame, self.frame)
        else:
            return 'undefined, length = {}'.format(self.length)
