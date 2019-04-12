def opcode(instruction):
    return instruction >> 12


def trapcode(instruction):
    return instruction & 0xFF


def sign_extend(x, bit_count):
    if (x >> (bit_count - 1)) & 1:
        x |= 0xFFFF << bit_count
    return x & 0xffff
