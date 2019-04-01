import ctypes


def opcode(instruction):
    return instruction >> 12


def trapcode(instruction):
    return instruction & 0xFF


def ushort(data):
    """Returns an unsigned short (16bit) representation of data."""
    return ctypes.c_ushort(data).value


def sign_extend(x, bit_count):
    """Extends number of bits for positive or negative x."""
    tmp = x >> (bit_count - 1) & 1
    if (tmp):
        x = x | (0xFFFF << bit_count)
    return ushort(x)
