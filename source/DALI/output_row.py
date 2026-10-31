"""The result of decoding a DALI frame: one row of the output, every column a string.

Every command code names its standard on its own, so a single command can refer
to another edition than the others of its table, e.g. when it was deprecated.
"""

from typing import NamedTuple

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


class OutputRow(NamedTuple):
    """The columns of the output for one DALI frame.

    Deprecated, reserved and unknown commands leave standard and clause empty.
    """

    data: str
    address: str
    command: str
    standard: str = ""
    clause: str = ""

    @staticmethod
    def lookup(
        table: dict[int, tuple[str, str, str]], opcode: int, unknown: str
    ) -> tuple[str, str, str]:
        """Command, standard and clause of the table, or the unknown text alone."""
        return table.get(opcode, (unknown, "", ""))
