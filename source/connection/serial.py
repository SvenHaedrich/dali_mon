import serial
import logging
import queue
import threading
import time
from .status import DaliStatus
from .frame import DaliFrame


logger = logging.getLogger(__name__)


class DaliSerial:
    DEFAULT_BAUDRATE = 115200
    QUEUE_MAXSIZE = 40

    def __init__(self, portname, baudrate=DEFAULT_BAUDRATE, transparent=False):
        logger.debug("open serial port")
        self.queue = queue.Queue(maxsize=self.QUEUE_MAXSIZE)
        self.port = serial.Serial(port=portname, baudrate=baudrate, timeout=0.2)
        self.transparent = transparent
        self.keep_running = False
        self.rx_frame = None

    @staticmethod
    def parse(line: str):
        try:
            start = line.find(ord("{")) + 1
            end = line.find(ord("}"))
            payload = line[start:end]
            timestamp = int(payload[0:8], 16) / 1000.0
            if payload[8] == ord(">"):
                loopback = True
            elif payload[8] == ord(":"):
                loopback = False
            else:
                raise ValueError
            length = int(payload[9:11], 16)
            data = int(payload[12:20], 16)
            return (timestamp, loopback, length, data)
        except ValueError:
            return None

    def read_worker_thread(self):
        logger.debug("read_worker_thread started")
        while self.keep_running:
            line = self.port.readline()
            if self.transparent:
                print(line.decode("utf-8"), end="")
            if len(line) > 0:
                logger.debug(f"received line <{line}> from serial")
                self.queue.put(self.parse(line))
        logger.debug("read_worker_thread terminated")

    def start_receive(self):
        if not self.keep_running:
            logger.debug("start receive")
            self.keep_running = True
            self.thread = threading.Thread(target=self.read_worker_thread, args=())
            self.thread.daemon = True
            self.thread.start()

    def get_next(self, timeout=None):
        logger.debug("get next")
        if not self.keep_running:
            logger.error("read thread is not running")
        try:
            result = self.queue.get(block=True, timeout=timeout)
        except queue.Empty:
            self.rx_frame = DaliFrame(status=DaliStatus(status=DaliStatus.TIMEOUT))
            return
        if result is None:
            self.rx_frame = DaliFrame(status=DaliStatus(status=DaliStatus.GENERAL))
            return
        self.rx_frame = DaliFrame(
            timestamp=result[0],
            length=result[2],
            data=result[3],
            status=DaliStatus(result[1], result[2], result[3]),
        )
        return

    def transmit(self, frame: DaliFrame, block: bool = False):
        if frame.send_twice:
            command = f"S{frame.priority} {frame.length:X}+{frame.data:X}\r".encode(
                "utf-8"
            )
        else:
            command = f"S{frame.priority} {frame.length:X} {frame.data:X}\r".encode(
                "utf-8"
            )
        logger.debug(f"write <{command}>")
        self.port.write(command)
        if block:
            self.get_next(5)

    def query_reply(self, frame: DaliFrame):
        if not self.keep_running:
            logger.error("read thread is not running")
        logger.debug("flush queue")
        while not self.queue.empty():
            self.queue.get()
        if frame.send_twice:
            command = f"Q{frame.priority} {frame.length:X}+{frame.data:X}\r".encode(
                "utf-8"
            )
        else:
            command = f"Q{frame.priority} {frame.length:X} {frame.data:X}\r".encode(
                "utf-8"
            )
        logger.debug(f"write <{command}>")
        self.port.write(command)
        logger.debug("read loopback")
        self.get_next(timeout=1)
        if (
            self.rx_frame.status.status != DaliStatus.LOOPBACK
            or self.rx_frame.data != frame.data
            or self.rx_frame.length != frame.length
        ):
            return
        logger.debug("read backframe")
        self.get_next(timeout=1)

    def close(self):
        logger.debug("close connection")
        if not self.keep_running:
            logger.debug("read thread is not running")
            return
        self.keep_running = False
        while self.thread.is_alive():
            time.sleep(0.001)
        logger.debug("connection closed, thread terminated")
