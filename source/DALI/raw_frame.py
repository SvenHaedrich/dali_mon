import logging

logger = logging.getLogger(__name__)

class Raw_Frame:
    COMMAND = '-'
    ERROR = '*'
    INVALID = ' '

    def reset_self(self):
        self.timestamp = 0
        self.type = self.INVALID
        self.length = 0
        self.data = 0


    def from_line(self, line):
        if self.echo:
            print(line.decode('utf-8'), end='')
        try:
            start = line.find(ord('{'))+1
            end = line.find(ord('}'))
            payload = line[start:end]
            self.timestamp = int(payload[0:8], 16) / 1000.0
            self.type = chr(payload[8])
            self.length = int(payload[9:11], 16)
            self.data = int(payload[12:20], 16)
        except ValueError:
            self.reset_self()
            self.type = self.INVALID
        logger.debug(F"Raw frame, length {self.length} data 0x{self.data:08X}")


    def __init__(self, echo=False):
        self.echo = echo
        self.reset_self()
