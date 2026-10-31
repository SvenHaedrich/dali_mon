"""The base class of the decoders, and the standards their commands refer to.

The command tables of the decoders name the standard for each command, so a
single command can refer to another edition than the rest of its table, e.g. a
command that was removed from the current edition.
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
    """The texts of a decoded DALI frame, one getter for each column of the output.

    The decoders derive from this class and set _address, _command, _standard and
    _reference in their __init__, data() gives the frame data with DATA_DIGITS hex
    digits. Standard and reference are both empty for reserved and unknown commands
    and for PHYSICAL SELECTION, which was removed before the editions of 2014.
    Commands removed later refer to the edition that defined them. eDALI frames
    have the standard eDALI and no reference, eDALI has no clauses.
    """

    # number of hex digits of the frame data
    DATA_DIGITS = 8

    def __init__(self, frame: DaliFrame) -> None:
        self.frame = frame
        self._address = ""
        self._command = ""
        self._standard = ""
        self._reference = ""

    def data(self) -> str:
        return f"{self.frame.data:0{self.DATA_DIGITS}X}"

    def address(self) -> str:
        return self._address

    def command(self) -> str:
        return self._command

    def standard(self) -> str:
        return self._standard

    def reference(self) -> str:
        return self._reference

    @staticmethod
    def lookup(
        table: dict[int, tuple[str, str, str]], opcode: int, unknown: str
    ) -> tuple[str, str, str]:
        """Command, standard and clause of the table, or the unknown text alone."""
        return table.get(opcode, (unknown, "", ""))
