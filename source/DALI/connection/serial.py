import logging

import serial  # type: ignore

from .dali_interface import DaliInterface
from .frame import DaliFrame
from .status import DaliStatus

logger = logging.getLogger(__name__)


class DaliSerial(DaliInterface):
    DEFAULT_BAUDRATE = 500000

    def __init__(self, portname, baudrate=DEFAULT_BAUDRATE, transparent=False):
        super().__init__()
        logger.debug("open serial port")
        self.port = serial.Serial(port=portname, baudrate=baudrate, timeout=0.2)
        self.port.set_low_latency_mode(True)
        self.transparent = transparent

    @staticmethod
    def parse(line: str) -> DaliFrame | None:
        try:
            start = line.find("{") + 1
            end = line.find("}")
            payload = line[start:end]
            timestamp = int(payload[0:8], 16) / 1000.0
            if payload[8] == ">":
                loopback = True
            else:
                loopback = False
            length = int(payload[9:11], 16)
            data = int(payload[12:20], 16)
            return DaliFrame(
                timestamp=timestamp,
                length=length,
                data=data,
                status=DaliStatus(loopback, length, data),
            )
        except ValueError:
            return None

    def read_data(self):
        line = self.port.readline().decode("utf-8").strip()
        if self.transparent:
            print(line, end="")
        if len(line) > 0:
            logger.debug(f"received line <{line}> from serial")
            self.queue.put(self.parse(line))

    def transmit(self, frame: DaliFrame, block: bool = False, is_query=False):
        command_byte = "Q" if is_query else "S"
        if frame.send_twice:
            command = f"{command_byte}{frame.priority} {frame.length:X}+{frame.data:X}\r"
        else:
            if frame.length == 8:
                command = f"Y{frame.data:X}\r"
            else:
                command = f"{command_byte}{frame.priority} {frame.length:X} {frame.data:X}\r"
        self.port.write(command.encode("utf-8"))
        logger.debug(f"write <{command.strip()}>")
        if block:
            self.get_next(self.RECEIVE_TIMEOUT)
