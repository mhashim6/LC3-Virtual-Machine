from memory import mem_read, mem_write, reg_read, reg_write, Registers
from utils import *
from traps import trap_routine


class Flags:
    POS = 1 << 0  # positive
    ZRO = 1 << 1  # zero
    NEG = 1 << 2  # negative


def update_flags(reg_index):
    reg_value = reg_read(reg_index)
    if reg_value == 0:
        reg_write(Registers.COND, Flags.ZRO)
    elif reg_value >> 15:  # a 1 in the left-most bit indicates negative.
        reg_write(Registers.COND, Flags.NEG)
    else:
        reg_write(Registers.COND, Flags.POS)


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
        reg_write(DR, reg_read(SR1) + imm5)
    else:
        SR2 = instruction & 0x7
        reg_write(DR, reg_read(SR1) + reg_read(SR2))

    update_flags(DR)


def _LD(instruction):
    """load"""
    DR = (instruction >> 9) & 0x7
    pc_offset = sign_extend(instruction & 0x1ff, 9)
    reg_write(DR,  mem_read(reg_read(Registers.PC) + pc_offset))
    update_flags(DR)


def _ST(instruction):
    """store"""
    DR = (instruction >> 9) & 0x7
    pc_offset = sign_extend(instruction & 0x1ff, 9)
    mem_write(reg_read(Registers.PC) + pc_offset, reg_read(DR))


# updates PC value by offset or new value
def _JSR(instruction):
    """jump register"""
    pc_reg = reg_read(Registers.PC)  # read current pc value
    # R7=current pc is the linkage back to the calling routine
    reg_write(Registers.R7, pc_reg)
    # check bit 11 if 1 or 0
    if ((instruction >> 11) & 0x0001) == 1:
        # compute and extend the immediate offset
        PCoffset = sign_extend(instruction & 0x07FF, 11)
        # update pc value by adding offset
        reg_write(Registers.PC, PCoffset+pc_reg)

    else:
        baseREG = (instruction >> 6) & 0x0007
        reg_value = reg_read(baseREG)  # read value in base register
        reg_write(Registers.PC, reg_value)  # update pc value by new value


def _AND(instruction):
    """bitwise and"""
    # compute the index of distination register
    dis_reg = (instruction >> 9) & 0x0007
    # compute the index of source1 register
    source1 = (instruction >> 6) & 0x0007

    if (instruction & 0x0020) >= 1:  # check bit 6
        # compute and extend the immediate value
        imm5 = sign_extend(instruction & 0x001F, 5)
        # compute output value in case bit6 == 1
        value = reg_read(source1) & imm5
        # update dist ination register value
        reg_write(dis_reg, value)
    else:
        # compute the index of source2 register
        source2 = instruction & 0x0007
        # compute output value in case bit6 == 0
        value = reg_read(source1) & reg_read(source2)
        # update dist ination register value
        reg_write(dis_reg, value)


def _LDR(instruction):
    """load register"""
    # compute the index of distination register
    dis_reg = (instruction >> 9) & 0x0007
    # compute the index of BaseR register
    BaseR = (instruction >> 6) & 0x0007
    # compute and extention offset6 value
    offset6 = sign_extend(instruction & 0x003F, 6)
    # compute memory addresse
    mem_addresse = reg_read(BaseR) + offset6
    # read the memory storage value
    value = mem_read(mem_addresse)
    # write value to distination register
    reg_write(dis_reg, value)
    # update flags
    update_flags(dis_reg)


def _STR(instruction):
    """store register"""
    # compute the index of source register
    SR_reg = (instruction >> 9) & 0x0007
    # compute the index of BaseR registe
    BaseR = (instruction >> 6) & 0x0007
    # compute and extention offset6 value
    offset6 = sign_extend(instruction & 0x003F, 6)
    # read the new memory storage value
    value = reg_read(SR_reg)
    # compute memory addresse
    mem_addresse = reg_read(BaseR) + offset6
    # write new value to memory
    mem_write(mem_addresse, value)


def _RTI(instruction):
    raise Exception("instruction is not implemented !")


def _NOT(instruction):
    # Destination Register.
    DR = (instruction >> 9) & 0X7
    # Source Register (register cntaining the data).
    SR = (instruction >> 6) & 0X7
    # every bit in the DR will equal to the flipped one with the same index in SR.
    reg_write(DR, ~reg_read(SR))
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
    reg_write(DR, mem_read(mem_read(address)))
    # store the sign of the last excuted instruction data (which is in the DR).
    update_flags(DR)


def _STI(instruction):
    # Source Register (the register containing the data).
    SR = (instruction >> 9) & 0x7
    # the value of what called an offset (embedded within the instruction code).
    PCoffset = sign_extend(instruction & 0x1ff, 9)
    # the address of the address that the data will be stored at.
    address = reg_read(Registers.PC) + PCoffset
    # write the data (stored in the SR) into the memory (the address is explained in the previous line).
    mem_write(mem_read(address), reg_read(SR))


def _JMP(instruction):
    """jump"""
    br = (instruction >> 6) & 0x7  # base register.
    reg_write(Registers.PC, reg_read(br))


def _RES(instruction):
    """reserved"""
    pass


def _LEA(instruction):
    """load effective address"""
    dr = (instruction >> 9) & 0x7
    pc_offset = sign_extend(instruction & 0x1ff, 9)
    address = pc_offset + reg_read(Registers.PC)
    reg_write(dr, address)
    update_flags(dr)


def _TRAP(instruction):
    trap_routine(trapcode(instruction))()


class OPCodes:
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
    return lambda: _instructions[_opcode](instruction)


def execute(instruction):
    _instruction_routine(instruction)()
