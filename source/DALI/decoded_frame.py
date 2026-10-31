"""The base class of the decoders, which take a DALI frame and give its texts.

Every command code names its standard on its own, so a single command can refer
to another edition than the others of its table, e.g. when it was deprecated.
"""

from dali_interface import DaliFrame

IEC_62386_101 = "IEC 62386-101:2022"
IEC_62386_102 = "IEC 62386-102:2022"
IEC_62386_103 = "IEC 62386-103:2022"
IEC_62386_105 = "IEC 62386-105:2020"
IEC_62386_207 = "IEC 62386-207:2018"
IEC_62386_208 = "IEC 62386-208:2009"
IEC_62386_209 = "IEC 62386-209:2011"
IEC_62386_301 = "IEC 62386-301:2017"
IEC_62386_302 = "IEC 62386-302:2017"
IEC_62386_303 = "IEC 62386-303:2017"
IEC_62386_304 = "IEC 62386-304:2017"
# older editions, for commands that were removed later
IEC_62386_102_2014 = "IEC 62386-102:2014"
IEC_62386_103_2014 = "IEC 62386-103:2014"
# eDALI frames are not part of IEC 62386
EDALI = "eDALI"


class DecodedFrame:
    """The texts of a decoded DALI frame, read by the getters.

    The decoders set address, command, standard and clause in their __init__.
    Deprecated, reserved and unknown commands leave standard and clause empty.
    """

    # number of hex digits of the frame data
    DATA_DIGITS = 8

    def __init__(self, frame: DaliFrame) -> None:
        self.frame = frame
        self._address = ""
        self._command = ""
        self._standard = ""
        self._clause = ""

    def data(self) -> str:
        return f"{self.frame.data:0{self.DATA_DIGITS}X}"

    def address(self) -> str:
        return self._address

    def command(self) -> str:
        return self._command

    def standard(self) -> str:
        return self._standard

    def clause(self) -> str:
        return self._clause

    @staticmethod
    def lookup(
        table: dict[int, tuple[str, str, str]], opcode: int, unknown: str
    ) -> tuple[str, str, str]:
        """Command, standard and clause of the table, or the unknown text alone."""
        return table.get(opcode, (unknown, "", ""))
