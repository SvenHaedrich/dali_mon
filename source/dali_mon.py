import sys
import logging
import click
from datetime import datetime
from termcolor import cprint

import DALI
from connection.status import DaliStatus
from connection.serial import DaliSerial
from connection.hid import DaliUsb

logger = logging.getLogger(__name__)


def print_local_time_color(enabled):
    if enabled:
        time_string = datetime.now().strftime("%H:%M:%S")
        cprint(f"{time_string} | ", color="yellow", end="")


def print_local_time(enabled):
    if enabled:
        time_string = datetime.now().strftime("%H:%M:%S")
        print(f"{time_string} | ", end="")


def print_command_color(absolute_time, timestamp, delta, dali_command):
    print_local_time_color(absolute_time)
    cprint(
        f"{timestamp:.03f} | {delta:8.03f} | {dali_command} | ", color="green", end=""
    )
    cprint(f"{dali_command.cmd()}", color="white")


def print_command(absolute_time, timestamp, delta, dali_command):
    print_local_time(absolute_time)
    print(f"{timestamp:.03f} | {delta:8.03f} | {dali_command} | {dali_command.cmd()}")


def print_error_color(absolute_time, timestamp, delta, status):
    print_local_time_color(absolute_time)
    cprint(f"{timestamp:.03f} | {delta:8.03f} | ", color="green", end="")
    cprint(f"{status.message}", color="red")


def print_error(absolute_time, timestamp, delta, status):
    print_local_time(absolute_time)
    print(f"{timestamp:.03f} | {delta:8.03f} | {status.message}")


def process_line(frame, no_color, absolute_time):
    if process_line.last_timestamp != 0:
        delta = frame.timestamp - process_line.last_timestamp
    else:
        delta = 0
    if frame.status.status in (DaliStatus.OK, DaliStatus.FRAME, DaliStatus.LOOPBACK):
        dali_command = DALI.Decode(
            frame.length, frame.data, process_line.active_device_type
        )
        if no_color:
            print_command(absolute_time, frame.timestamp, delta, dali_command)
        else:
            print_command_color(absolute_time, frame.timestamp, delta, dali_command)
            process_line.active_device_type = dali_command.get_next_device_type()
    else:
        if no_color:
            print_error(absolute_time, frame.timestamp, delta, frame.status)
        else:
            print_error_color(absolute_time, frame.timestamp, delta, frame.status)
    process_line.last_timestamp = frame.timestamp


def main_usb(no_color, absolute_time):
    logger.debug("read from Lunatone usb device")
    dali_connection = DaliUsb()
    dali_connection.start_receive()
    try:
        while True:
            dali_connection.get_next()
            process_line(dali_connection.rx_frame, no_color, absolute_time)
    except KeyboardInterrupt:
        print("\rinterrupted")
        dali_connection.close()


def main_tty(transparent, no_color, absolute_time):
    logger.debug("read from tty device")
    line = ""
    while True:
        line = line + sys.stdin.readline()
        if len(line) > 0 and line[-1] == "\n":
            line = line.strip(" \r\n")
            if len(line) > 0:
                frame = DaliSerial.parse(line.encode("utf-8"))
                process_line(frame, no_color, absolute_time)
            line = ""


def main_file(transparent, no_color, absolute_time):
    logger.debug("read from file")
    for line in sys.stdin:
        if len(line) > 0:
            frame = DaliSerial.parse(line.encode("utf-8"))
            process_line(frame, no_color, absolute_time)


@click.command()
@click.version_option("1.1.2")
@click.option(
    "-l",
    "--hid",
    help="Use USB HID class connector for DALI communication.",
    is_flag=True,
)
@click.option("--debug", help="Enable debug level logging.", is_flag=True)
@click.option("--nocolor", help="Do not use color coding for output.", is_flag=True)
@click.option("--echo", help="Echo unprocessed input line to output.", is_flag=True)
@click.option("--absolute", help="Add absolute local time to output.", is_flag=True)
def dali_mon(hid, debug, nocolor, echo, absolute):
    """
    Monitor for DALI commands,
    SevenLabs 2023
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    process_line.last_timestamp = 0
    process_line.active_device_type = DALI.DeviceType.NONE
    try:
        if hid:
            main_usb(nocolor, absolute)
        elif sys.stdin.isatty():
            main_tty(echo, nocolor, absolute)
        else:
            main_file(echo, nocolor, absolute)
    except KeyboardInterrupt:
        print("\rinterrupted")


if __name__ == "__main__":
    dali_mon()
