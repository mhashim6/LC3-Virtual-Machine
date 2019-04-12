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


def _BR(instruction):
    """branch"""
    pc_offset = sign_extend((instruction) & 0x1ff, 9)
    cond_flag = (instruction >> 9) & 0x7
    if cond_flag & reg_read(Registers.COND):
        reg_write(Registers.PC, (reg_read(Registers.PC) + pc_offset))


def _ADD(instruction):
    """add"""
    # destination register DR
    DR = (instruction >> 9) & 0x7
    # first operand SR1
    SR1 = (instruction >> 6) & 0x7
    # for immediate mode
    imm_flag = (instruction >> 5) & 0x1

    if imm_flag:
        imm5 = sign_extend(instruction & 0x1F, 5)
        reg_write(Registers(DR), reg_read(Regisers(SR1)) + imm5)
    else:
        SR2 = instruction & 0x7
        reg_write(Registers(DR), reg_read(
            Registers(SR1)) + reg_read(Registers(SR2)))

    update_flags(DR)


def _LD(instruction):
    """load"""
    DR = (instruction >> 9) & 0x7
    pc_offset = sign_extend(instruction & 0x1ff, 9)
    reg_write(Registers(DR),  mem_read(reg_read(Regisers.PC) + pc_offset))
    update_flags(DR)


def _ST(instruction):
    """store"""
    DR = (instruction >> 9) & 0x7
    pc_offset = sign_extend(instruction & 0x1ff, 9)
    mem_write(reg_read(Registers.PC) + pc_offset), Registers(DR)


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
    br = (instruction >> 6) & 0x7  # base register.
    reg_write(Registers.PC, reg_read(Registers(br)))


def _RES(instruction):
    """reserved"""
    pass


def _LEA(instruction):
    """load effective address"""
    dr = (instruction >> 9) & 0x7
    pc_offset = sign_extend(instruction & 0x1ff, 9)
    address = pc_offset + reg_read(Registers.PC)
    reg_write(Registers(dr), address)
    update_flags(dr)


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
    OPCodes.OP_JSR: _JSR,
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
    reg_write(Registers.PC, reg_read(Registers.PC) + 1)
