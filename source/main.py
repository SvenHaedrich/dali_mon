import getopt
import sys
from datetime import datetime

import serial
from termcolor import cprint

import dali
import dali_error
import line
import sender


def main(serial_port, input_filename, use_color, absolute_time):
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
                    if absolute_time:
                        cprint('{} : '.format(datetime.now().strftime("%H:%M:%S")), color='yellow', end='')
                    cprint('{:.03f} : {:8.03f} : {} : '.format(input_line.timestamp, delta, dali_frame), color='green',
                           end='')
                    cprint('{}'.format(dali_frame.cmd()), color='white')
                else:
                    if absolute_time:
                        print('{} : '.format(datetime.now().strftime("%H:%M:%S")), end='')
                    print('{:.03f} : {:8.03f} : {} : {}'.format(input_line.timestamp, delta, dali_frame,
                                                                dali_frame.cmd()))
                active_device_type = dali_frame.enable
            else:
                if use_color:
                    if absolute_time:
                        cprint('{} : '.format(datetime.now().strftime("%H:%M:%S")), color='yellow', end='')
                    cprint('{:.03f} : {:8.03f} : '.format(input_line.timestamp, delta), color='green', end='')
                    cprint('{}'.format(dali_error.DALIError(input_line.length, input_line.data)), color='red')
                else:
                    if absolute_time:
                        print('{} : '.format(datetime.now().strftime("%H:%M:%S")), end='')
                    print('{:.03f} : {:8.03f} : {}'.format(input_line.timestamp, delta,
                                                           dali_error.DALIError(input_line.length, input_line.data)))
            last_timestamp = input_line.timestamp
    my_port.close()


def show_version():
    print('dali_py version 1.0.2')


def show_help():
    show_version()
    print('usage: -h : help')
    print('       --help')
    print('       -p <port> : use port')
    print('       --port')
    print('       -f <name>: send file name')
    print('       --file')
    print('       -v : show version information')
    print('       --version')
    print('       --nocolor : don\'t use colors')
    print('       --absolute : add stamp with absolute time')
    print('output colums:')
    print('       if enabled: absolute timestamp (from this machine)')
    print('       relative timestamp in seconds (from interface)')
    print('       delta time to previous command')
    print('       hex data received')
    print('       DALI command translation')


# - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    port = '/dev/ttyUSB2'
    filename = ''
    verbose = False
    color = True
    absolute_time = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hpfv:', ['help', 'port=', 'file=', 'version', 'nocolor', 'absolute'])
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
            show_version()
        if opt == '--nocolor':
            color = False
        if opt == '--absolute':
            absolute_time = True

    main(port, filename, color, absolute_time)
