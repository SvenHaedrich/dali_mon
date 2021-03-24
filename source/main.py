import getopt
import sys

import serial

import dali
import dali_error
import line
import sender
from termcolor import cprint


def main(serial_port, input_filename, use_color):
    my_port = serial.Serial(port=serial_port, baudrate=115200)
    my_file = sender.Sender(file_name=input_filename, serial_port=my_port)
    last_timestamp = 0
    delta = 0
    active_device_type = dali.DeviceTypes.NONE
    while True:
        my_file.send_next_line()
        input_line = line.Line(my_port.readline())
        if not input_line.type == input_line.INVALID:
            if last_timestamp != 0:
                delta = input_line.timestamp - last_timestamp
            if input_line.type == input_line.COMMAND:
                dali_frame = dali.Frame(input_line.length, input_line.data, active_device_type)
                if use_color:
                    cprint('{:.03f} : {:8.03f} : {} : '.format(input_line.timestamp, delta, dali_frame), color='green',
                           end='')
                    cprint('{}'.format(dali_frame.cmd()), color='white')
                else:
                    print('{:.03f} : {:8.03f} : {} : {}'.format(input_line.timestamp, delta, dali_frame,
                                                                dali_frame.cmd()))
                active_device_type = dali_frame.enable
            else:
                if use_color:
                    cprint('{:.03f} : {:8.03f} : '.format(input_line.timestamp, delta), color='green', end='')
                    cprint('{}'.format(dali_error.DALIError(input_line.length, input_line.data)), color='red')
                else:
                    print('{:.03f} : {:8.03f} : {}'.format(input_line.timestamp, delta,
                                                           dali_error.DALIError(input_line.length, input_line.data)))
            last_timestamp = input_line.timestamp
    my_port.close()


def show_help():
    print('usage: -h : help')
    print('       --help')
    print('       -p <port> : use port')
    print('       --port')
    print('       -f <name>: send file name')
    print('       --file')
    print('       -v : show version information')
    print('       --version')
    print('       --nocolor : don\'t use colors')


# - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    port = '/dev/ttyUSB2'
    filename = ''
    verbose = False
    color = True
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hpfvn:', ['help', 'port=', 'file=', 'version', 'nocolor'])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            show_help()
            sys.exit()
        if opt in ('-p', '--port'):
            port = arg
        if opt in ('-f', '--file'):
            filename = arg
        if opt in ('-v', '--version'):
            print('dali_py version 1.0.2')
        if opt == '--nocolor':
            color = False

    main(port, filename, color)
