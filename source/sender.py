import time

class Sender:

    def __init__(self, file_name='', serial_port=''):
        self.active = False
        if not file_name == '':
            try:
                self.my_file = open(file_name, 'rb')
                self.active = True
            except IOError:
                self.active = False
        self.serial_port = serial_port
        if serial_port == '':
            self.active = False

    def send_next_line(self):
        if self.active:
            line = self.my_file.readline()
            if line == b'':
                self.active = False
                self.my_file.close()
                return
            command = line.decode('ascii').split('#')
            command = command[0].strip()
            if command == 'W' or command == "w":
                time.sleep(2.0)
            else:
                command += '\r'
                self.serial_port.write(command.encode('ascii'))
            return
