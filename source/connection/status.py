class DaliStatus:
    OK = 0
    LOOPBACK = 1
    FRAME = 2
    TIMEOUT = 3
    TIMING = 4
    INTERFACE = 5
    FAILURE = 6
    GENERAL = 7
    UNDEFINED = 8

    def built_message(self, message="ERROR", data=0):
        bit = data & 0x0FF
        timer_us = (data >> 8) & 0x0FFFFF
        return f"ERROR: FRAME {message} - BIT: {bit} - TIME: {timer_us} USEC"

    def __init__(self, loopback=False, length=0, data=0, status=None):
        if status is None:
            if length in range(0, 0x21):
                if loopback:
                    self.status = DaliStatus.LOOPBACK
                    self.message = "LOOPBACK FRAME"
                else:
                    self.status = DaliStatus.FRAME
                    self.message = "NOMRAL FRAME"
            elif length in range(0x81) or length == 0x92:
                self.status = DaliStatus.OK
                self.message = "OK"
            elif length == 0x81:
                self.status = DaliStatus.TIMEOUT
                self.message = "TIMEOUT"
            elif length == 0x82:
                self.status = DaliStatus.TIMING
                self.message = self.built_message("START", data)
            elif length == 0x83:
                self.status = DaliStatus.TIMING
                self.message = self.built_message("DATA", data)
            elif length in (0x84, 0x85, 0x86):
                self.status = DaliStatus.TIMING
                self.message = "ERROR: COLLISION DETECTED"
            elif length == 0x91:
                self.status = DaliStatus.FAILURE
                self.message = "ERROR: SYSTEM FAILURE"
            elif length in (0xA0, 0xA1, 0xA2, 0xA3):
                self.status = DaliStatus.INTERFACE
                self.message = "ERROR: INTERFACE"
            else:
                self.status = DaliStatus.UNDEFINED
                self.message = f"ERROR: CODE 0x{length:02X}"
        else:
            self.status = status
            message_dictionary = {
                0: "OK",
                1: "LOOPBACK",
                2: "NORMAL FRAME",
                3: "TIMEOUT",
                4: "ERROR: TIMING",
                5: "ERROR: INTERFACE",
                6: "ERROR: FAILURE",
                7: "ERROR: GENERAL",
            }
            if status in message_dictionary:
                self.message = message_dictionary[status]
            else:
                self.message = f"ERROR: CODE 0x{status:02X}"
