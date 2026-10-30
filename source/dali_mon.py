#!/usr/bin/env python3

import errno
import logging
import os
import select
import sys
import tomllib
from datetime import datetime
from pathlib import Path

import click
from click.core import ParameterSource
from dali_interface import (
    DaliFrame,
    DaliInterface,
    DaliSerial,
    DaliStatus,
    DaliUsb,
)
from termcolor import cprint

from DALI.decode import Decode
from DALI.forward_frame_16bit import DeviceType

logger = logging.getLogger(__name__)

PYPROJECT = Path(__file__).resolve().parent.parent / "pyproject.toml"
with PYPROJECT.open("rb") as pyproject:
    VERSION = tomllib.load(pyproject)["project"]["version"]


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
    cprint(f"{address:<22} {command}", color="white", end="")
    cprint("")


def print_error(
    absolute_time: float, timestamp: float, delta_s: float, message: str
) -> None:
    print_local_time(absolute_time)
    cprint(f"{timestamp:.03f} | {delta_s:8.03f} | ", color="green", end="")
    cprint(f"{message}", color="red")


def process_line(frame: DaliFrame | None, absolute_time: float) -> None:
    if frame is None:
        return
    if process_line.last_timestamp != 0:
        delta_s = frame.timestamp - process_line.last_timestamp
    else:
        delta_s = 0
    if frame.status in (DaliStatus.OK, DaliStatus.FRAME, DaliStatus.LOOPBACK):
        decoding = Decode(frame, process_line.active_device_type)
        data, address, command = decoding.get_strings()
        print_command(absolute_time, frame.timestamp, delta_s, data, address, command)
        process_line.active_device_type = decoding.get_next_device_type()
    else:
        print_error(absolute_time, frame.timestamp, delta_s, frame.message)
    process_line.last_timestamp = frame.timestamp


def exit_with_error(message: str) -> None:
    cprint(f"\r{message}", color="red", file=sys.stderr)
    sys.exit(1)


def open_connection(open_interface, name: str) -> DaliInterface:
    try:
        return open_interface()
    except (OSError, ValueError) as error:
        # pyusb raises USBError without an error number
        reason = str(error).removeprefix("[Errno None] ")
        exit_with_error(f"cannot open {name}: {reason}")


# time to wait for a frame before checking that the connection is still alive
GET_TIMEOUT_S = 0.5


class EchoFrame(DaliFrame):
    """DALI frame together with the unprocessed input line, for --echo.
    A line without DALI information gives a frame that is only echoed."""

    line = ""
    is_dali = True


class DaliSerialEcho(DaliSerial):
    """Serial interface that passes the unprocessed input lines on for --echo.
    They travel with the frames through the receive queue, so the main thread
    prints them in order with the decoded frames."""

    def read_frame(self) -> DaliFrame | None:
        line = self.port.readline().decode(encoding="ascii", errors="ignore").strip()
        if len(line) == 0:
            return None
        frame = self.parse(line)
        echo = EchoFrame(*frame) if frame else EchoFrame(status=DaliStatus.OK)
        echo.line = line
        echo.is_dali = frame is not None
        return echo


def main_connection(
    absolute_time: bool, connection: DaliInterface, on: bool, off: bool
) -> None:
    logger.debug("read from connection")
    try:
        try:
            if on:
                connection.power(True)
            if off:
                connection.power(False)
        except RuntimeError:
            exit_with_error("power control not supported")
        try:
            while True:
                frame = connection.get(timeout=GET_TIMEOUT_S)
                # no frame within the timeout
                if frame.status == DaliStatus.TIMEOUT:
                    continue
                if isinstance(frame, EchoFrame):
                    print(frame.line)
                    if not frame.is_dali:
                        continue
                process_line(frame, absolute_time)
        except RuntimeError as error:
            # the receive thread of the interface stopped
            exit_with_error(f"connection lost: {error.__cause__ or error}")
    finally:
        connection.close()


def process_tty_line(line: str, transparent: bool, absolute_time: bool) -> None:
    line = line.strip(" \r\n")
    if len(line) > 0:
        if transparent:
            print(line)
        process_line(DaliSerial.parse(line), absolute_time)


def main_tty(transparent: bool, absolute_time: bool) -> None:
    logger.debug("read from tty device")
    stdin = sys.stdin.fileno()
    poller = select.poll()
    poller.register(stdin, select.POLLIN)
    pending = ""
    while True:
        events = 0
        for _, event in poller.poll():
            events |= event
        try:
            data = os.read(stdin, 4096)
        except OSError as error:
            if error.errno != errno.EIO:
                raise
            data = b""
            events |= select.POLLHUP
        if len(data) == 0:
            if events & (select.POLLHUP | select.POLLERR):
                exit_with_error("connection lost: device hung up")
            continue
        pending = pending + data.decode(encoding="ascii", errors="ignore")
        *lines, pending = pending.split("\n")
        for line in lines:
            process_tty_line(line, transparent, absolute_time)


def main_file(transparent: bool, absolute_time: bool) -> None:
    logger.debug("read from file")
    for line in sys.stdin:
        if len(line) > 0:
            if transparent:
                print(line, end="")
            frame = DaliSerial.parse(line)
            process_line(frame, absolute_time)


@click.command(name="dali_mon")
@click.version_option(VERSION, prog_name="dali_mon")
@click.option(
    "-l",
    "--hid",
    help="Use USB HID class connector for DALI communication.",
    envvar="DALI_HID_USB",
    show_envvar=True,
    is_flag=True,
)
@click.option("--debug", help="Enable debug level logging.", hidden=True, is_flag=True)
@click.option("--echo", help="Echo unprocessed input line to output.", is_flag=True)
@click.option("--absolute", help="Add absolute local time to output.", is_flag=True)
@click.option("--on", help="Enable power supply (if available).", is_flag=True)
@click.option("--off", help="Disable power supply (if available).", is_flag=True)
@click.option(
    "-s",
    "--serial-port",
    help="Serial port used for DALI communication.",
    envvar="DALI_SERIAL_PORT",
    show_envvar=True,
    type=click.Path(exists=True, dir_okay=False),
)
def dali_mon(hid, debug, echo, absolute, serial_port, on, off):
    """
    Monitor for DALI commands.
    sevenlab engineering 2026
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    if hid and serial_port:
        # an option on the command line overrides an environment variable
        context = click.get_current_context()
        hid_given = context.get_parameter_source("hid") == ParameterSource.COMMANDLINE
        port_given = (
            context.get_parameter_source("serial_port") == ParameterSource.COMMANDLINE
        )
        if hid_given == port_given:
            raise click.UsageError("--hid and --serial-port exclude each other.")
        if hid_given:
            serial_port = None
        else:
            hid = False
    if on and off:
        raise click.UsageError("--on and --off exclude each other.")
    if (on or off) and not hid:
        raise click.UsageError(f"{'--on' if on else '--off'} needs --hid.")
    if echo and hid:
        raise click.UsageError("--echo needs stdin or --serial-port, not --hid.")

    process_line.last_timestamp = 0
    process_line.active_device_type = DeviceType.NONE
    try:
        if hid:
            connection = open_connection(DaliUsb, "DALI USB converter")
            main_connection(absolute, connection, on, off)
        elif serial_port:
            serial_class = DaliSerialEcho if echo else DaliSerial
            connection = open_connection(
                lambda: serial_class(serial_port), f"serial port {serial_port}"
            )
            main_connection(absolute, connection, on, off)
        elif sys.stdin.isatty():
            main_tty(echo, absolute)
        else:
            main_file(echo, absolute)
    except KeyboardInterrupt:
        # Ctrl-C is the expected end of a connection
        print("\rinterrupted", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    dali_mon(prog_name="dali_mon")
