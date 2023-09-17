#!/usr/bin/env python3

import sys
import logging
import click
import datetime
from termcolor import cprint

from DALI.connection.status import DaliStatus
from DALI.connection.frame import DaliFrame
from DALI.connection.serial import DaliSerial
from DALI.forward_frame_16bit import DeviceType
from DALI.decode import Decode

logger = logging.getLogger(__name__)


def print_local_time(enabled: bool) -> None:
    if enabled:
        time_string = datetime.now().strftime("%H:%M:%S")
        cprint(f"{time_string} | ", color="yellow", end="")


def print_command(
    absolute_time: float,
    timestamp: float,
    delta_s: float,
    data: str,
    address: str,
    command: str,
) -> None:
    print_local_time(absolute_time)
    cprint(f"{timestamp:.03f} | {delta_s:8.03f} | {data:>8} | ", color="green", end="")
    cprint(f"{address:<20} {command}", color="white", end="")
    cprint("")


def print_error(
    absolute_time: float, timestamp: float, delta_s: float, status: DaliStatus
) -> None:
    print_local_time(absolute_time)
    cprint(f"{timestamp:.03f} | {delta_s:8.03f} | ", color="green", end="")
    cprint(f"{status.message}", color="red")


def process_line(frame: DaliFrame, absolute_time: float) -> None:
    if process_line.last_timestamp != 0:
        delta_s = frame.timestamp - process_line.last_timestamp
    else:
        delta_s = 0
    if frame.status.status in (DaliStatus.OK, DaliStatus.FRAME, DaliStatus.LOOPBACK):
        decoding = Decode(frame, process_line.active_device_type)
        data, address, command = decoding.get_strings()
        print_command(absolute_time, frame.timestamp, delta_s, data, address, command)
        process_line.active_device_type = decoding.get_next_device_type()
    else:
        print_error(absolute_time, frame.timestamp, delta_s, frame.status)
    process_line.last_timestamp = frame.timestamp


def main_usb(absolute_time: bool) -> None:
    logger.debug("read from Lunatone usb device")
    dali_connection = DaliUsb()
    dali_connection.start_receive()
    try:
        while True:
            dali_connection.get_next()
            process_line(dali_connection.rx_frame, absolute_time)
    except KeyboardInterrupt:
        print("\rinterrupted")
        dali_connection.close()


def main_tty(transparent: bool, absolute_time: bool) -> None:
    logger.debug("read from tty device")
    line = ""
    while True:
        line = line + sys.stdin.readline()
        if len(line) > 0 and line[-1] == "\n":
            line = line.strip(" \r\n")
            if len(line) > 0:
                frame = DaliSerial.parse(line.encode("utf-8"))
                process_line(frame, absolute_time)
            line = ""


def main_file(transparent: bool, absolute_time: bool) -> None:
    logger.debug("read from file")
    for line in sys.stdin:
        if len(line) > 0:
            frame = DaliSerial.parse(line)
            process_line(frame, absolute_time)


@click.command()
@click.version_option("1.5.0")
@click.option(
    "-l",
    "--hid",
    help="Use USB HID class connector for DALI communication.",
    is_flag=True,
)
@click.option("--debug", help="Enable debug level logging.", is_flag=True)
@click.option("--echo", help="Echo unprocessed input line to output.", is_flag=True)
@click.option("--absolute", help="Add absolute local time to output.", is_flag=True)
def dali_mon(hid: bool, debug: bool, echo: bool, absolute: bool) -> None:
    """
    Monitor for DALI commands,
    SevenLab 2023
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    process_line.last_timestamp = 0
    process_line.active_device_type = DeviceType.NONE
    try:
        if hid:
            main_usb(absolute)
        elif sys.stdin.isatty():
            main_tty(echo, absolute)
        else:
            main_file(echo, absolute)
    except KeyboardInterrupt:
        print("\rinterrupted")


if __name__ == "__main__":
    dali_mon()
