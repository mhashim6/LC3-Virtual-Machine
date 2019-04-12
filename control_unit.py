from memory import *
from utils import *
from enum import Enum
from traps import trap_routine


class Flags(Enum):
    POS = 1 << 0  # positive
    ZRO = 1 << 1  # zero
    NEG = 1 << 2  # negative


def update_flags(reg_index):
    reg_value = Registers(reg_index).value
    if reg_value == 0:
        reg_write(Registers.COND, Flags.ZRO.value)
    elif reg_value >> 15:  # a 1 in the left-most bit indicates negative.
        reg_write(Registers.COND, Flags.NEG.value)
    else:
        reg_write(Registers.COND, Flags.POS.value)


def _BR(instruction):
    """branch"""
    pc_offset = sign_extend(instruction & 0x1ff, 9)
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
        reg_write(Registers(DR), reg_read(Registers(SR1)) + imm5)
    else:
        SR2 = instruction & 0x7
        reg_write(Registers(DR), reg_read(
            Registers(SR1)) + reg_read(Registers(SR2)))

    update_flags(DR)


def _LD(instruction):
    """load"""
    DR = (instruction >> 9) & 0x7
    pc_offset = sign_extend(instruction & 0x1ff, 9)
    reg_write(Registers(DR),  mem_read(reg_read(Registers.PC) + pc_offset))
    update_flags(DR)


def _ST(instruction):
    """store"""
    DR = (instruction >> 9) & 0x7
    pc_offset = sign_extend(instruction & 0x1ff, 9)
    mem_write(reg_read(Registers.PC) + pc_offset), reg_read(Registers(DR))


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
    # Destination Register.
    DR = (instruction >> 9) & 0X7
    # Source Register (register cntaining the data).
    SR = (instruction >> 6) & 0X7
    # every bit in the DR will equal to the flipped one with the same index in SR.
    reg_write(Registers(DR), ~reg_read(Registers(SR)))
    # store the sign of the last excuted instruction data (which is in the DR).
    update_flags(DR)


def _LDI(instruction):
    # Destenation Register.
    DR = (instruction >> 9) & 0x7
    # the value of what called an offset (embedded within the instruction code).
    PCoffset = sign_extend(instruction & 0X1ff, 9)
    # the address of the address of the desired data.
    address = reg_read(Registers.PC) + PCoffset
    # write the data (its address is explained in the previous line) in the register (DR).
    reg_write(Registers(DR), mem_read(mem_read(address)))
    # store the sign of the last excuted instruction data (which is in the DR).
    update_flags(DR)


def _STI(instruction):
    # Source Register (the register containing the data).
    SR = (instruction >> 9) & 0x7
    # the value of what called an offset (embedded within the instruction code).
    PCoffset = sign_extend((instruction) & 0x1ff, 9)
    # the address of the address that the data will be stored at.
    address = reg_read(Registers.PC) + PCoffset
    # write the data (stored in the SR) into the memory (the address is explained in the previous line).
    mem_write(mem_read(address), reg_read(Registers(SR)))


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


def _TRAP(instruction):
    trap_routine(trapcode(instruction))()


class OPCodes(Enum):
    BR = 0       # branch
    ADD = 1      # add
    LD = 2       # load
    ST = 3       # store
    JSR = 4      # jump register
    AND = 5      # bitwise and
    LDR = 6      # load register
    STR = 7      # store register
    RTI = 8      # unused
    NOT = 9      # bitwise not
    LDI = 10     # load indirect
    STI = 11     # store indirect
    JMP = 12     # jump
    RES = 13     # reserved (unused)
    LEA = 14     # load effective address
    TRAP = 15    # execute trap


_instructions = {
    OPCodes.BR: _BR,
    OPCodes.ADD: _ADD,
    OPCodes.LD: _LD,
    OPCodes.ST: _ST,
    OPCodes.JSR: _JSR,
    OPCodes.AND: _AND,
    OPCodes.LDR: _LDR,
    OPCodes.STR: _STR,
    OPCodes.RTI: _RTI,
    OPCodes.NOT: _NOT,
    OPCodes.LDI: _LDI,
    OPCodes.STI: _STI,
    OPCodes.JMP: _JMP,
    OPCodes.RES: _RES,
    OPCodes.LEA: _LEA,
    OPCodes.TRAP: _TRAP
}


def _instruction_routine(instruction):
    _opcode = opcode(instruction)
    # print(OPCodes(_opcode))
    return lambda: _instructions[OPCodes(_opcode)](instruction)


def execute(instruction):
    _instruction_routine(instruction)()
