class DALIError:
    OK = 0
    RECEIVE_START_TIMING = 1
    RECEIVE_DATA_TIMING = 2
    LOOPBACK_TIME = 3
    NO_CHANGE = 4
    WRONG_STATE = 5
    SETTLING_TIME_VIOLATION = 6
    SYSTEM_IDLE = 11
    SYSTEM_FAILUTE = 12
    SYSTEM_RECOVER = 13
    CAN_NOT_PROCESS = 20
    BAD_ARGUMENT = 21
    QUEUE_FULL = 22
    BAD_COMMAND = 23

    def __init__(self, error_code=0, data=0):
        self.data = data
        self.error_code = error_code
        error_dictionary = {self.OK: 'OK',
                            self.RECEIVE_START_TIMING: 'ERROR: RECEIVE START TIMING',
                            self.RECEIVE_DATA_TIMING: 'ERROR: RECEIVE DATA TIMING',
                            self.LOOPBACK_TIME: 'ERROR: LOOPBACK TIME',
                            self.NO_CHANGE: 'ERROR: NO CHANGE',
                            self.WRONG_STATE: 'ERROR: WRONG STATE',
                            self.SETTLING_TIME_VIOLATION: 'ERROR: SETTLING TIME VIOLATION',
                            self.SYSTEM_IDLE: 'ERROR: SYSTEM IDLE',
                            self.SYSTEM_FAILUTE: 'ERROR: SYSTEM FAILURE',
                            self.SYSTEM_RECOVER: 'ERROR: SYSTEM RECOVER',
                            self.CAN_NOT_PROCESS: 'ERROR: CAN NOT PROCESS',
                            self.BAD_ARGUMENT: 'ERROR: BAD ARGUMENT',
                            self.QUEUE_FULL: 'ERROR: QUEUE FULL',
                            self.BAD_COMMAND: 'ERROR: BAD COMMAND',
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
