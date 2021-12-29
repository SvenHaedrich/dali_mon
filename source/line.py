class Line:
    COMMAND = '-'
    ERROR = '*'
    INVALID = ' '

    def reset_self(self):
        self.timestamp = 0
        self.type = self.INVALID
        self.length = 0
        self.data = 0

    def __init__(self, input_line, echo=False):
        self.reset_self()
        if echo:
            print(input_line.decode('utf-8'), end='')
        try:
            start = input_line.find(ord('{'))+1
            end = input_line.find(ord('}'))
            payload = input_line[start:end]
            self.timestamp = int(payload[0:8], 16) / 1000.0
            self.type = chr(payload[8])
            self.length = int(payload[9:11], 16)
            self.data = int(payload[12:20], 16)
        except ValueError:
            self.reset_self()
            self.type = self.INVALID
            return
