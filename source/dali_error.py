class msg:

    def __init__ (self,error_code=0,data=0):
        self.data = data
        error_dictionary = {0:'OK',
                            1:'ERROR: RECEIVE START TIMING',
                            2:'ERROR: RECEIVE DATA TIMINIG',
                            3:'ERROR: LOOPBACK TIME',
                            4:'ERROR: NO CHANGE',
                            5:'ERROR: WRONG STATE',
                            6:'ERROR: SETTLING TIME VIOLATION'
                           }
        if error_code in error_dictionary:
            self.msg = error_dictionary[error_code]
        else:
            self.msg = 'UNDEFINED ERROR CODE'

    def __str__ (self):
        bit = self.data & 0x0ff
        timer_us = (self.data >> 8) & 0x0fffff
        result = '{} - BIT: {} - TIME: {} USEC'.format(self.msg,bit,timer_us)
        return result