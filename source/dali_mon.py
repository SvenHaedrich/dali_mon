#!/usr/bin/env python3

import errno
import logging
import os
import select
import sys
import tomllib
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import NoReturn

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
from DALI.output_row import OutputRow

logger = logging.getLogger(__name__)

PYPROJECT = Path(__file__).resolve().parent.parent / "pyproject.toml"
with PYPROJECT.open("rb") as pyproject:
    VERSION = tomllib.load(pyproject)["project"]["version"]


# widths of the columns, the longest texts over all frames; the clause is the last
# column and needs no width
DATA_WIDTH = 8
ADDRESS_WIDTH = 22
COMMAND_WIDTH = 59
STANDARD_WIDTH = 18


@dataclass
class OutputOptions:
    """What is shown besides the decoded frames."""

    # the local time in front of each frame, --absolute
    absolute_time: bool = False
    # the unprocessed input line before each frame, --echo
    echo: bool = False
    # the standard and the clause that define the command
    show_standard: bool = True
    show_clause: bool = True


output = OutputOptions()


def print_local_time() -> None:
    if output.absolute_time:
        time_string = datetime.now().strftime("%H:%M:%S")
        cprint(f"{time_string} | ", color="yellow", end="")


def print_command(timestamp: float, delta_s: float, row: OutputRow) -> None:
    print_local_time()
    cprint(
        f"{timestamp:.03f} | {delta_s:8.03f} | {row.data:>{DATA_WIDTH}} | ",
        color="green",
        end="",
    )
    if not (output.show_standard or output.show_clause):
        cprint(f"{row.address:<{ADDRESS_WIDTH}} {row.command}", color="white")
        return
    cprint(
        f"{row.address:<{ADDRESS_WIDTH}} {row.command:<{COMMAND_WIDTH}}",
        color="white",
        end="",
    )
    references = ""
    if output.show_standard:
        references += f" | {row.standard:<{STANDARD_WIDTH}}"
    if output.show_clause:
        references += f" | {row.clause}"
    cprint(references.rstrip(), color="cyan")


def print_error(timestamp: float, delta_s: float, message: str) -> None:
    print_local_time()
    cprint(f"{timestamp:.03f} | {delta_s:8.03f} | ", color="green", end="")
    cprint(f"{message}", color="red")


@dataclass
class DecoderState:
    """What process_line keeps from one frame to the next."""

    last_timestamp: float = 0
    active_device_type: int = DeviceType.NONE


state = DecoderState()


def process_line(frame: DaliFrame | None) -> None:
    if frame is None:
        return
    if state.last_timestamp != 0:
        delta_s = frame.timestamp - state.last_timestamp
    else:
        delta_s = 0
    if frame.status in (DaliStatus.OK, DaliStatus.FRAME, DaliStatus.LOOPBACK):
        decoding = Decode(frame, state.active_device_type)
        print_command(frame.timestamp, delta_s, decoding.output_row())
        state.active_device_type = decoding.get_next_device_type()
    else:
        print_error(frame.timestamp, delta_s, frame.message)
    state.last_timestamp = frame.timestamp


def exit_with_error(message: str) -> NoReturn:
    cprint(f"\r{message}", color="red", file=sys.stderr)
    sys.exit(1)


def open_connection(
    open_interface: Callable[[], DaliInterface], name: str
) -> DaliInterface:
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
        # the receive thread drops timeout frames, so a timeout line travels
        # as a frame that is only echoed
        if frame is not None and frame.status != DaliStatus.TIMEOUT:
            echo = EchoFrame(**frame._asdict())
            echo.is_dali = True
        else:
            echo = EchoFrame(status=DaliStatus.OK)
            echo.is_dali = False
        echo.line = line
        return echo


def main_connection(connection: DaliInterface, on: bool, off: bool) -> None:
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
                process_line(frame)
        except RuntimeError as error:
            # the receive thread of the interface stopped
            exit_with_error(f"connection lost: {error.__cause__ or error}")
    finally:
        connection.close()


def process_tty_line(line: str) -> None:
    line = line.strip(" \r\n")
    if len(line) > 0:
        if output.echo:
            print(line)
        process_line(DaliSerial.parse(line))


def main_tty() -> None:
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
            process_tty_line(line)


def main_file() -> None:
    logger.debug("read from file")
    for line in sys.stdin:
        if len(line) > 0:
            if output.echo:
                print(line, end="")
            frame = DaliSerial.parse(line)
            process_line(frame)


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
@click.option(
    "--no-standard", help="Hide the standard that defines a command.", is_flag=True
)
@click.option(
    "--no-clause", help="Hide the clause that defines a command.", is_flag=True
)
@click.option(
    "--no-reference", help="Hide standard and clause of a command.", is_flag=True
)
@click.option("--on", help="Enable power supply (if available).", is_flag=True)
@click.option("--off", help="Disable power supply (if available).", is_flag=True)
@click.option(
    "-s",
    "--serial-port",
    help="Serial port used for DALI communication.",
    envvar="DALI_SERIAL_PORT",
    show_envvar=True,
    type=click.Path(dir_okay=False),
)
def dali_mon(
    hid: bool,
    debug: bool,
    echo: bool,
    absolute: bool,
    serial_port: str | None,
    on: bool,
    off: bool,
    no_standard: bool,
    no_clause: bool,
    no_reference: bool,
) -> None:
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
    if serial_port:
        # check the port only when it is used, --hid overrides DALI_SERIAL_PORT
        context = click.get_current_context()
        parameter = next(p for p in context.command.params if p.name == "serial_port")
        click.Path(exists=True, dir_okay=False).convert(serial_port, parameter, context)

    output.absolute_time = absolute
    output.echo = echo
    output.show_standard = not (no_standard or no_reference)
    output.show_clause = not (no_clause or no_reference)
    state.last_timestamp = 0
    state.active_device_type = DeviceType.NONE
    try:
        if hid:
            connection = open_connection(DaliUsb, "DALI USB converter")
            main_connection(connection, on, off)
        elif serial_port:
            serial_class = DaliSerialEcho if output.echo else DaliSerial
            connection = open_connection(
                lambda: serial_class(serial_port), f"serial port {serial_port}"
            )
            main_connection(connection, on, off)
        elif sys.stdin.isatty():
            main_tty()
        else:
            main_file()
    except KeyboardInterrupt:
        # Ctrl-C is the expected end of a connection
        print("\rinterrupted", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    dali_mon(prog_name="dali_mon")
