"""The standards a decoded command refers to, and where it is defined in them.

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


class Reference(NamedTuple):
    """The standard and the clause that define a command."""

    standard: str
    clause: str


class Command(NamedTuple):
    """A command with the standard and the clause it is defined in.

    Deprecated, reserved and unknown commands have no standard and no clause.
    """

    name: str
    standard: str = ""
    clause: str = ""


def lookup(table: dict[int, Command], opcode: int, unknown: str) -> Command:
    """The command of the table, or the unknown text without a reference."""
    return table.get(opcode, Command(unknown))
