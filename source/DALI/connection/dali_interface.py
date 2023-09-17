import logging
import queue
import threading
import time

from .frame import DaliFrame
from .status import DaliStatus

logger = logging.getLogger(__name__)


class DaliInterface:
    RECEIVE_TIMEOUT = 1

    def __init__(self, max_queue_size: int = 40):
        self.queue: queue.Queue = queue.Queue(maxsize=max_queue_size)
        self.keep_running = False
        self.rx_frame: DaliFrame | None = None

    def read_data(self):
        raise NotImplementedError("subclass must implement read_data")

    def read_worker_thread(self):
        logger.debug("read_worker_thread started")
        while self.keep_running:
            self.read_data()
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
            self.rx_frame = self.queue.get(block=True, timeout=timeout)
        except queue.Empty:
            self.rx_frame = DaliFrame(status=DaliStatus(status=DaliStatus.TIMEOUT))
            return
        if self.rx_frame is None:
            self.rx_frame = DaliFrame(status=DaliStatus(status=DaliStatus.GENERAL))
            return

    def transmit(self, frame: DaliFrame, block: bool = False, is_query=False):
        raise NotImplementedError("subclass must implement transmit")

    def query_reply(self, frame: DaliFrame):
        if not self.keep_running:
            logger.error("read thread is not running")
        logger.debug("flush queue")
        while not self.queue.empty():
            self.queue.get()
        self.transmit(frame, False, True)
        logger.debug("read loopback")
        self.get_next(timeout=self.RECEIVE_TIMEOUT)
        if (
            not self.rx_frame
            or self.rx_frame.status.status != DaliStatus.LOOPBACK
            or self.rx_frame.data != frame.data
            or self.rx_frame.length != frame.length
        ):
            return
        logger.debug("read backframe")
        self.get_next(timeout=self.RECEIVE_TIMEOUT)

    def close(self):
        logger.debug("close connection")
        if not self.keep_running:
            logger.debug("read thread is not running")
            return
        self.keep_running = False
        while self.thread.is_alive():
            time.sleep(0.001)
        logger.debug("connection closed, thread terminated")
