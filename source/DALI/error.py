class DALIError:
    GENERAL = 9
    FRAME = 10
    RECOVER = 8


    def __init__(self, error_code=0, data=0):
        self.data = data
        self.error_code = error_code
        error_dictionary = {0: 'OK',
                            1: 'ERROR: RECEIVE START TIMING',
                            2: 'ERROR: RECEIVE DATA TIMING',
                            3: 'ERROR: LOOPBACK TIME',
                            4: 'ERROR: NO CHANGE',
                            5: 'ERROR: WRONG STATE',
                            6: 'ERROR: SETTLING TIME VIOLATION',
                            11: 'ERROR: SYSTEM IDLE',
                            12: 'ERROR: SYSTEM FAILURE',
                            13: 'ERROR: SYSTEM RECOVER',
                            20: 'ERROR: CAN NOT PROCESS',
                            21: 'ERROR: BAD ARGUMENT',
                            22: 'ERROR: QUEUE FULL',
                            23: 'ERROR: BAD COMMAND',
                            }
        if error_code in error_dictionary:
            self.msg = error_dictionary[error_code]
        else:
            self.msg = F'UNDEFINED ERROR CODE ({error_code})'

    def __str__(self):
        bit = self.data & 0x0ff
        timer_us = (self.data >> 8) & 0x0fffff
        if self.error_code < 7:
            return F'{self.msg} - BIT: {bit} - TIME: {timer_us} USEC'
        else:
            return self.msg
