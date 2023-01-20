import sys
import logging
import click
from datetime import datetime
from termcolor import cprint

import DALI
import dali_usb


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


def print_error_color(absolute_time, raw, delta):
    print_local_time_color(absolute_time)
    cprint(f"{raw.timestamp:.03f} | {delta:8.03f} | ", color="green", end="")
    cprint(f"{DALI.DALIError(raw.length, raw.data)}", color="red")


def print_error(absolute_time, raw, delta):
    print_local_time(absolute_time)
    print(
        f"{raw.timestamp:.03f} | {delta:8.03f} | {DALI.DALIError(raw.length, raw.data)}"
    )


def process_line(raw, use_color, absolute_time):
    if not raw.type == raw.INVALID:
        if process_line.last_timestamp != 0:
            delta = raw.timestamp - process_line.last_timestamp
        else:
            delta = 0
        if raw.type == raw.COMMAND:
            dali_command = DALI.Decode(raw, process_line.active_device_type)
            if use_color:
                print_command_color(absolute_time, raw.timestamp, delta, dali_command)
            else:
                print_command(absolute_time, raw.timestamp, delta, dali_command)
            process_line.active_device_type = dali_command.get_next_device_type()
        else:
            if use_color:
                print_error_color(absolute_time, raw, delta)
            else:
                print_error(absolute_time, raw, delta)
        process_line.last_timestamp = raw.timestamp


def main_usb(color, absolute_time):
    dali_connection = dali_usb.DALI_Usb()
    dali_connection.start_read()
    try:
        while True:
            raw_frame = dali_connection.read_raw_frame()
            process_line(raw_frame, color, absolute_time)
    except KeyboardInterrupt:
        print("\rinterrupted")
        dali_connection.close()


def main_tty(transparent, color, absolute_time):
    raw = DALI.Raw_Frame(transparent)
    while True:
        line = sys.stdin.readline()
        if len(line) > 0:
            line = line.encode("utf-8")
            raw.from_line(line)
            process_line(raw, color, absolute_time)


def main_file(transparent, color, absolute_time):
    raw = DALI.Raw_Frame(transparent)
    for line in sys.stdin:
        if len(line) > 0:
            line = line.encode("utf-8")
            raw.from_line(line)
            process_line(raw, color, absolute_time)


@click.command()
@click.version_option("1.1.0")
@click.option(
    "-l",
    "--lunatone",
    help="Try to use a Lunatone USB connector for DALI communication.",
    is_flag=True,
)
@click.option("--debug", help="Enable debug level logging.", is_flag=True)
@click.option("--nocolor", help="Do not use color coding for output.", is_flag=True)
@click.option("--echo", help="Echo unprocessed input line to output.", is_flag=True)
@click.option("--absolute", help="Add absolute local time to output.", is_flag=True)
def dali_mon(lunatone, debug, nocolor, echo, absolute):
    """
    Monitor for DALI commands,
    SevenLabs 2023
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    if nocolor:
        color = False
    else:
        color = True

    process_line.last_timestamp = 0
    process_line.active_device_type = DALI.DeviceType.NONE
    try:
        if lunatone:
            main_usb(color, absolute)
        elif sys.stdin.isatty():
            main_tty(echo, color, absolute)
        else:
            main_file(echo, color, absolute)
    except KeyboardInterrupt:
        print("\rinterrupted")


if __name__ == "__main__":
    dali_mon()
