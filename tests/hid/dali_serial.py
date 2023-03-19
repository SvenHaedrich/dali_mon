import serial
import logging
import queue
import threading
import time
import DALI

logger = logging.getLogger(__name__)


class DALI_Serial:
    DEFAULT_BAUDRATE = 115200
    QUEUE_MAXSIZE = 40

    def __init__(self, port, baudrate=DEFAULT_BAUDRATE, transparent=False):
        logger.debug("open serial port")
        self.queue = queue.Queue(maxsize=self.QUEUE_MAXSIZE)
        self.port = serial.Serial(port=port, baudrate=baudrate)
        self.keep_running = False
        self.transparent = transparent

    def read_worker_thread(self):
        logger.debug("read_worker_thread started")
        raw = DALI.Raw_Frame(self.transparent)
        while self.keep_runnning:
            line = self.port.readline()
            logger.debug(f"received line <{line}> from serial")
            raw.from_line(line)
            self.queue.put(raw)
        logger.debug("read_worker_thread terminated")

    def start_read(self):
        logger.debug("start read")
        self.keep_runnning = True
        self.thread = threading.Thread(target=self.read_worker_thread, args=())
        self.thread.daemon = True
        self.thread.start()

    def read_raw_frame(self, timeout=None):
        return self.queue.get(block=True, timeout=timeout)

    @staticmethod
    def convert_raw_frame_to_serial_command(frame, priority=2):
        if frame.send_twice:
            return f"T{priority} {frame.length:X} {frame.data:X}\r".encode("utf-8")
        else:
            return f"S{priority} {frame.length:X} {frame.data:X}\r".encode("utf-8")

    def write(self, frame):
        logger.debug("write frame")
        self.port.write(self.convert_raw_frame_to_serial_command(frame))

    def close(self):
        logger.debug("close connection")
        if self.keep_running:
            self.keep_running = False
            while self.thread.is_alive():
                time.sleep(0.001)
