import serial
import logging
import queue
import threading
import raw_frame

logger = logging.getLogger(__name__)


class Dali_Serial:
    DEFAULT_PORT = "/dev/ttyUSB0"
    DEFAULT_BAUDRATE = 115200
    QUEUE_MAXSIZE = 40
    

    def __init__(self,port=DEFAULT_PORT, baudrate=DEFAULT_BAUDRATE, transparent=False):

        logger.debug("Open serial port")
        self.queue = queue.Queue(maxsize=self.QUEUE_MAXSIZE)
        self.port = serial.Serial(port=port, baudrate=baudrate)
        self.worker_runnuing = False
        self.transparent = transparent


    def read_worker_thread(self):
        logger.debug("read_worker_thread started")
        raw = raw_frame.Raw_Frame(self.transparent)
        while self.worker_runnning:
            line = self.port.readline()
            logger.debug("received a line from serial")
            raw.from_line(line)
            self.queue.put(raw)
            

    def start_read(self):
        logger.debug("Start read")
        self.worker_runnning = True
        thread = threading.Thread(target=self.read_worker_thread, args=())
        thread.daemon = True
        thread.start()   


    def read_raw_frame(self):
        return self.queue.get(block=True)


    def close(self):
        logger.debug("Close connection")
        self.worker_running = False
