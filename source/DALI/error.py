class DALIError:
    GENERAL = 9
    FRAME = 10
    RECOVER = 8

    def __init__(self, error_code=0, data=0):
        self.data = data
        self.error_code = error_code
        error_dictionary = {
            0: "OK",
            1: "ERROR: RECEIVE START TIMING",
            2: "ERROR: RECEIVE DATA TIMING",
            3: "ERROR: LOOPBACK TIME",
            4: "ERROR: NO CHANGE",
            5: "ERROR: WRONG STATE",
            6: "ERROR: SETTLING TIME VIOLATION",
            7: "ERROR: SYSTEM FAILURE",
            8: "ERROR: RECOVERED FROM FAILURE - BUS OK",
            9: "ERROR: GENERAL",
            10: "ERROR: FRAME",
        }
        if error_code in error_dictionary:
            self.msg = error_dictionary[error_code]
        else:
            self.msg = "UNDEFINED ERROR CODE"

    def __str__(self):
        bit = self.data & 0x0FF
        timer_us = (self.data >> 8) & 0x0FFFFF
        if self.error_code < 7:
            return f"{self.msg} - BIT: {bit} - TIME: {timer_us} USEC"
        else:
            return self.msg
