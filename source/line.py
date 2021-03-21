class Line:

    COMMAND = '-'
    ERROR = '*'
    INVALID = ' '

    def reset_self(self):
        self.timestamp = 0
        self.type = self.INVALID
        self.length = 0
        self.data = 0

    def __init__(self,input_line):
        self.reset_self()
        try:
            self.timestamp = int(input_line[1:9], 16)/1000.0
            self.type = chr(input_line[10])
            self.length = int(input_line[11:13], 16)
            self.data =  int(input_line [14:22], 16)
        except ValueError:
            self.reset_self()
            self.type = self.INVALID
            return
