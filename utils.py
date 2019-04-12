def opcode(instruction):
    return instruction >> 12


def trapcode(instruction):
    return instruction & 0xFF


def sign_extend(x, bit_count):
    """Extends number of bits for positive or negative x."""
    tmp = x >> (bit_count - 1) & 1
    if (tmp):
        x = x | (0xFFFF << bit_count)
    return ushort(x)
