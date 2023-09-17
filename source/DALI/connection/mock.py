import logging
from random import choice
from time import sleep

from ..gear_opcodes import GearOpcode
from .dali_interface import DaliInterface
from .frame import DaliFrame

logger = logging.getLogger(__name__)


class DaliMock(DaliInterface):
    def __init__(self):
        super().__init__()
        logger.debug("initialize mock interface")

    def read_data(self):
        sleep(1)
        address_byte = 0xFF  # broadcast address
        opcode_byte = choice(  # nosec B311
            [
                GearOpcode.OFF,
                GearOpcode.RECALL_MAX_LEVEL,
                GearOpcode.UP,
                GearOpcode.DOWN,
                GearOpcode.STEP_DOWN_AND_OFF,
                GearOpcode.ON_AND_STEP_UP,
            ]
        )
        logger.info(f"Generate frame with opcode {opcode_byte}")
        data = opcode_byte + (address_byte << 8)
        self.queue.put(DaliFrame(data=data, length=16))

    def transmit(self, frame: DaliFrame, block: bool = False, is_query=False):
        twice = "T" if frame.send_twice else "S"
        logger.info(f"{twice}{frame.priority} length:{frame.length:X} data:{frame.data:X}")
