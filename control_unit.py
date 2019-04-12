from memory import *
from utils import *
from enum import Enum
from traps import trap_routine


class Flags(Enum):
    POS = 1 << 0  # positive
    ZRO = 1 << 1  # zero
    NEG = 1 << 2  # negative


def update_flags(reg_index):
    reg_value = Registers(reg_index)
    if reg_value == 0:
        reg_write(Registers.COND, Flags.ZRO)
    elif reg_value >> 15:  # a 1 in the left-most bit indicates negative.
        reg_write(Registers.COND, Flags.NEG)
    else:
        reg_write(Registers.COND, Flags.POS)


class MMR(Enum):  # TODO
    """Memory-mapped registers """
    KBSR = 0xFFE00  # keyboard status
    KBDR = 0xFFE02  # keyboard data


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
    raise Exception("instruction is not implemented !")
    


def _NOT(instruction):
    DR = (instruction >> 9) & 0X7                                # Destination Register.
    SR = (instruction >> 6) & 0X7                                # Source Register (register cntaining the data).
    reg_write(Registers(DR), ~reg_read(Registers(SR)))             # every bit in the DR will equal to the flipped one with the same index in SR. 
    update_flags(DR)                                               # store the sign of the last excuted instruction data (which is in the DR).
    


def _LDI(instruction):
    DR = (instruction >> 9) & 0x7                                # Destenation Register.
    PCoffset = sign_extend((instruction) & 0X1ff, 9)               # the value of what called an offset (embedded within the instruction code).
    address = reg_read(Registers.PC) + PCoffset                    # the address of the address of the desired data.
    reg_write(Registers(DR), mem_read(mem_read(address)))          # write the data (its address is explained in the previous line) in the register (DR).
    update_flags(DR)                                               # store the sign of the last excuted instruction data (which is in the DR).
    


def _STI(instruction):
    SR = ((instruction) >> 9) & 0x7                                # Source Register (the register containing the data).
    PCoffset = sign_extend((instruction) & 0x1ff, 9)               # the value of what called an offset (embedded within the instruction code).
    address = reg_read(Registers.PC) + PCoffset                    # the address of the address that the data will be stored at.
    mem_write(mem_read(address), reg_read(Registers(SR)))          # write the data (stored in the SR) into the memory (the address is explained in the previous line).
    


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
    _opcode = opcode(instruction)
    if _opcode == OPCodes.OP_TRAP.value:  # it's a trap!
        return lambda: trap_routine(trapcode(instruction))
    return lambda: _instructions[OPCodes(_opcode)](instruction)  # phew!


def execute(instruction):
    _instruction_routine(instruction)()
    # increment PC by #1.
    reg_write(Registers.PC, ushort(reg_read(Registers.PC) + 1))
