import serial
import dali
import sys
import getopt
import dali_error
import line
import sender


def main(serial_port,input_filename):
    print('# dali_py')
    print('# interpret results from dali_usb connector')
    print('# version 1.0.1')
    print('# user serial: {}'.format(serial_port))
    my_port = serial.Serial(port=serial_port, baudrate=115200)
    my_file = sender.Sender(file_name=input_filename, serial_port=my_port)
    if my_file.active:
        print('# send file {}'.format(input_filename))
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
                dali_frame = dali.Frame(input_line.length,input_line.data,active_device_type)
                print('{:.03f} : {:8.03f} : {} : {}'.format(input_line.timestamp,delta,dali_frame,dali_frame.cmd()))
                active_device_type = dali_frame.enable
            else:
                print('{:.03f} : {:8.03f} : {}'.format(input_line.timestamp,delta,dali_error.msg(input_line.length,input_line.data)))
            last_timestamp = input_line.timestamp
    my_port.close()


def show_help():
    print('usage: -h : help')
    print('       --help')
    print('       -p <port> : use port')
    print('       --port')
    print('       -f <name>: send file name')
    print('       --file')


# - - - - - - - - - - - - - - - - - - - - 
if __name__ == '__main__':
    port = '/dev/ttyUSB2'
    filename = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:],'hpf:',['help','port=','file='])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h','--help'):
            show_help()
            sys.exit()
        if opt in ('-p','--port'):
            port = arg
        if opt in ('-f','--file'):
            filename = arg
    main(port,filename)

