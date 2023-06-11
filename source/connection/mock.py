import logging

logger = logging.getLogger(__name__)


class DaliMock:
    def __init__(self):
        logger.debug("initialize mock interface")
        self.last_transmit = None
        self.data = None

    def start_receive(self):
        logger.debug("start receive")

    def get_next(self, timeout=None):
        logger.debug("get next")
        return

    def transmit(self, frame, block=False):
        logger.debug("transmit")
        if frame.send_twice:
            print(f"T{frame.priority} {frame.length:X} {frame.data:X}")
        else:
            print(f"S{frame.priority} {frame.length:X} {frame.data:X}")
        self.last_transmit = frame.data
        self.data = frame.data
        self.length = frame.length

    def close(self):
        logger.debug("close mock interface")
