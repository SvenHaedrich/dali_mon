import errno
import logging
import queue
import struct
import threading
import time
import usb
from .status import DaliStatus
from .frame import DaliFrame

logger = logging.getLogger(__name__)


class DaliUsb:
    _USB_VENDOR = 0x17B5
    _USB_PRODUCT = 0x0020

    _USB_CMD_INIT = 0x01
    _USB_CMD_BOOTLOADER = 0x02
    _USB_CMD_SEND = 0x12
    _USB_CMD_SEND_ANSWER = 0x15
    _USB_CMD_SET_IOPINS = 0x20
    _USB_CMD_READ_IOPINS = 0x21
    _USB_CMD_IDENTIFY = 0x22
    _USB_CMD_POWER = 0x40

    _USB_CTRL_DAPC = 0x04
    _USB_CTRL_DEVTYPE = 0x80
    _USB_CTRL_SETDTR = 0x10
    _USB_CTRL_TWICE = 0x20
    _USB_CTRL_ID = 0x40

    _USB_WRITE_TYPE_NO = 0x01
    _USB_WRITE_TYPE_8BIT = 0x02
    _USB_WRITE_TYPE_16BIT = 0x03
    _USB_WRITE_TYPE_25BIT = 0x04
    _USB_WRITE_TYPE_DSI = 0x05
    _USB_WRITE_TYPE_24BIT = 0x06
    _USB_WRITE_TYPE_STATUS = 0x07
    _USB_WRITE_TYPE_17BIT = 0x08

    _USB_READ_MODE_INFO = 0x01
    _USB_READ_MODE_OBSERVE = 0x11
    _USB_READ_MODE_REPSONSE = 0x12

    _USB_READ_TYPE_NO_FRAME = 0x71
    _USB_READ_TYPE_8BIT = 0x72
    _USB_READ_TYPE_16BIT = 0x73
    _USB_READ_TYPE_25BIT = 0x74
    _USB_READ_TYPE_DSI = 0x75
    _USB_READ_TYPE_24BIT = 0x76
    _USB_READ_TYPE_INFO = 0x77
    _USB_READ_TYPE_17BIT = 0x78

    _USB_STATUS_CHECKSUM = 0x01
    _USB_STATUS_SHORTED = 0x02
    _USB_STATUS_FRAME_ERROR = 0x03
    _USB_STATUS_OK = 0x04
    _USB_STATUS_DSI = 0x05
    _USB_STATUS_DALI = 0x06

    def __init__(self, vendor=_USB_VENDOR, product=_USB_PRODUCT):
        # lookup devices by _USB_VENDOR and _USB_PRODUCT
        self.interface = 0
        self.queue = queue.Queue(maxsize=40)
        self.keep_running = False
        self.send_sequence_number = 1
        self.receive_sequence_number = None
        self.rx_frame = None

        logger.debug("try to discover DALI interfaces")
        devices = [
            dev
            for dev in usb.core.find(find_all=True, idVendor=vendor, idProduct=product)
        ]

        # if not found
        if devices:
            logger.info(f"DALI interfaces found: {devices}")
        else:
            raise usb.core.USBError("DALI interface not found")

        # use first device from list
        self.device = devices[0]
        self.device.reset()

        # detach kernel driver if necessary
        if self.device.is_kernel_driver_active(self.interface) is True:
            self.device.detach_kernel_driver(self.interface)

        self.device.set_configuration()
        usb.util.claim_interface(self.device, self.interface)
        cfg = self.device.get_active_configuration()
        intf = cfg[(0, 0)]

        # get read and write endpoints
        self.ep_write = usb.util.find_descriptor(
            intf,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)
            == usb.util.ENDPOINT_OUT,
        )
        self.ep_read = usb.util.find_descriptor(
            intf,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)
            == usb.util.ENDPOINT_IN,
        )
        if not self.ep_read or not self.ep_write:
            raise usb.core.USBError(
                f"could not determine read or write endpoint on {self.device}"
            )

        # read pending messages and discard
        try:
            while True:
                self.ep_read.read(self.ep_read.wMaxPacketSize, timeout=10)
                logger.info("DALI interface - disregard pending messages")
        except Exception:
            pass

    def read_raw(self, timeout=None):
        return self.ep_read.read(self.ep_read.wMaxPacketSize, timeout=timeout)

    def transmit(self, frame: DaliFrame, block: bool = False):
        command = self._USB_CMD_SEND
        self.send_sequence_number = (self.send_sequence_number + 1) & 0xFF
        sequence = self.send_sequence_number
        control = self._USB_CTRL_TWICE if frame.send_twice else 0
        if frame.length == 24:
            ext = (frame.data >> 16) & 0xFF
            address_byte = (frame.data >> 8) & 0xFF
            opcode_byte = frame.data & 0xFF
            write_type = self._USB_WRITE_TYPE_24BIT
        elif frame.length == 16:
            ext = 0x00
            address_byte = (frame.data >> 8) & 0xFF
            opcode_byte = frame.data & 0xFF
            write_type = self._USB_WRITE_TYPE_16BIT
        elif frame.length == 8:
            ext = 0x00
            address_byte = 0x00
            opcode_byte = frame.data & 0xFF
            write_type = self._USB_WRITE_TYPE_8BIT
        else:
            raise Exception(
                f"DALI commands must be 8,16 or 24 bit long. This is {frame.length} bit long"
            )

        logger.debug(
            f"DALI>OUT: CMD=0x{command:02X} SEQ=0x{sequence:02X} TYC=0x{write_type:02X} "
            f"EXT=0x{ext:02X} ADR=0x{address_byte:02X} OCB=0x{opcode_byte:02X}"
        )
        buffer = struct.pack(
            "BBBBxBBB" + (64 - 8) * "x",
            command,
            sequence,
            control,
            write_type,
            ext,
            address_byte,
            opcode_byte,
        )
        result = self.ep_write.write(buffer)
        self.last_transmit = frame.data

        if block:
            if not self.keep_running:
                raise Exception("receive must be active for blocking call to transmit.")
            else:
                self.get_next()
                if self.send_sequence_number != self.receive_sequence_number:
                    raise Exception("expected same sequence number.")
        return result

    def close(self):
        logger.debug("close connection")
        if not self.keep_running:
            logger.error("read thread is not running")
        self.keep_running = False
        while self.thread.is_alive():
            time.sleep(0.001)
        usb.util.dispose_resources(self.device)

    def read_worker_thread(self):
        logger.debug("read_worker_thread started")
        while self.keep_running:
            try:
                usb_data = self.read_raw(timeout=100)
                if usb_data:
                    read_type = usb_data[1]
                    receive_sequence_number = usb_data[8]
                    logger.debug(
                        f"DALI[IN]: SN=0x{usb_data[8]:02X} TY=0x{usb_data[1]:02X} "
                        f"EC=0x{usb_data[3]:02X} AD=0x{usb_data[4]:02X} OC=0x{usb_data[5]:02X}"
                    )
                    if read_type == self._USB_READ_TYPE_8BIT:
                        status = DaliStatus(status=DaliStatus.FRAME)
                        length = 8
                        dali_data = usb_data[5]
                    elif read_type == self._USB_READ_TYPE_16BIT:
                        status = DaliStatus(status=DaliStatus.FRAME)
                        length = 16
                        dali_data = usb_data[5] + (usb_data[4] << 8)
                    elif read_type == self._USB_READ_TYPE_24BIT:
                        status = DaliStatus(status=DaliStatus.FRAME)
                        length = 24
                        dali_data = (
                            usb_data[5] + (usb_data[4] << 8) + (usb_data[3] << 16)
                        )
                    elif read_type == self._USB_READ_TYPE_NO_FRAME:
                        status = DaliStatus(status=DaliStatus.TIMEOUT)
                        length = 0
                        dali_data = 0
                    elif read_type == self._USB_READ_TYPE_INFO:
                        length = 0
                        dali_data = 0
                        if usb_data[5] == self._USB_STATUS_OK:
                            status = DaliStatus(status=DaliStatus.OK)
                        elif usb_data[5] == self._USB_STATUS_FRAME_ERROR:
                            status = DaliStatus(status=DaliStatus.TIMING)
                        else:
                            status = DaliStatus(status=DaliStatus.GENERAL)
                    self.queue.put(
                        DaliFrame(
                            timestamp=time.time(),
                            length=length,
                            data=dali_data,
                            status=status,
                        )
                    )

            except usb.USBError as e:
                if e.errno not in (errno.ETIMEDOUT, errno.ENODEV):
                    raise e
        logger.debug("read_worker_thread terminated")

    def start_receive(self):
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

    def query_reply(self, frame: DaliFrame):
        if not self.keep_running:
            logger.error("read thread is not running")
        logger.debug("flash queue")
        while not self.queue.empty():
            self.queue.get()
        logger.debug("transmit command")
        self.transmit(frame)
        logger.debug("read loopback")
        self.get_next(timeout=1)
        if (
            self.rx_frame.status.status != DaliStatus.FRAME
            or self.rx_frame.data != frame.data
            or self.rx_frame.length != frame.length
        ):
            return
        logger.debug("read backframe")
        self.get_next(timeout=1)
