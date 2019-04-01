from memory import *
from utils import *
from enum import Enum
from traps import trap_routine


class Flags(Enum):
    FL_POS = 1 << 0  # positive
    FL_ZRO = 1 << 1  # zero
    FL_NEG = 1 << 2  # negative


class MMR(Enum):  # TODO
    """Memory-mapped registers """
    KBSR = 0xFFE00  # keyboard status
    KBDR = 0xFFE02  # keyboard data


class Halt(Exception):
    """Thrown to indicate HALT instruction has been executed."""
    pass


def _BR(instruction):
    """branch"""
    pass


def _ADD(instruction):
    """add"""
    pass


def _LD(instruction):
    """load"""
    pass


def _ST(instruction):
    """store"""
    pass


def _JSR(instruction):
    """jump register"""
    pass


def _AND(instruction):
    """bitwise and"""
    pass


def _LDR(instruction):
    """load register"""
    pass


def _STR(instruction):
    """store register"""
    pass


def _RTI(instruction):
    """unused"""
    pass  # TODO throw exception here.


def _NOT(instruction):
    """bitwise not"""
    pass


def _LDI(instruction):
    """load indirect"""
    pass


def _STI(instruction):
    """store indirect"""
    pass


def _JMP(instruction):
    """jump"""
    pass


def _RES(instruction):
    """reserved"""
    pass  # TODO throw exception here.


def _LEA(instruction):
    """load effective address"""
    pass


class OPCodes(Enum):
    OP_BR = 0       # branch
    OP_ADD = 1      # add
    OP_LD = 2       # load
    OP_ST = 3       # store
    OP_JSR = 4      # jump register
    OP_AND = 5      # bitwise and
    OP_LDR = 6      # load register
    OP_STR = 7      # store register
    OP_RTI = 8      # unused
    OP_NOT = 9      # bitwise not
    OP_LDI = 10     # load indirect
    OP_STI = 11     # store indirect
    OP_JMP = 12     # jump
    OP_RES = 13     # reserved (unused)
    OP_LEA = 14     # load effective address
    OP_TRAP = 15    # execute trap


_instructions = {
    OPCodes.OP_BR: _BR,
    OPCodes.OP_ADD: _ADD,
    OPCodes.OP_LD: _LD,
    OPCodes.OP_ST: _ST,
    OPCodes.OP_AND: _AND,
    OPCodes.OP_LDR: _LDR,
    OPCodes.OP_STR: _STR,
    OPCodes.OP_RTI: _RTI,
    OPCodes.OP_NOT: _NOT,
    OPCodes.OP_LDI: _LDI,
    OPCodes.OP_STI: _STI,
    OPCodes.OP_JMP: _JMP,
    OPCodes.OP_RES: _RES,
    OPCodes.OP_LEA: _LEA
}


def _instruction_routine(instruction):
    opcode = opcode(instruction)
    if opcode == OPCodes.OP_TRAP.value:  # it's a trap!
        return lambda: trap_routine(trapcode(instruction))
    return lambda: _instructions[OPCodes(opcode)](instruction)  # phew!


def execute(instruction):
    _instruction_routine(instruction)()
    # increment PC by #1.
    reg_write(Registers.PC, ushort(reg_read(Registers.PC) + 1))
