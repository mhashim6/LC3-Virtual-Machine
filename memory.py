from enum import Enum
import array
from kbhit import check_key
from platform_getch import getch

_MEMORY_SIZE = 2 ** 16
_main_memory = array.array('H', [0 for i in range(_MEMORY_SIZE)])


class MMR(Enum):
    """Memory-mapped registers """
    KBSR = 0xFE00  # keyboard status
    KBDR = 0xFE02  # keyboard data


def load_image(image):
    origin = image[0]
    # starting from #1 as we've already read #0, aka the origin,
    # which indicates the starting address of the program in memory.
    for i in range(1, len(image)):
        mem_write(origin + i, image[i])


def mem_write(address, value):
    _main_memory[address] = value % _MEMORY_SIZE


def mem_read(address):
    if address == MMR.KBSR.value:
        mem_write(MMR.KBSR.value, (1 << 15))
        mem_write(MMR.KBDR.value, ord(getch()))
    else:
        mem_write(MMR.KBSR.value, 0)

    return _main_memory[address]


class Registers(Enum):
    R0 = 0
    R1 = 1
    R2 = 2
    R3 = 3
    R4 = 4
    R5 = 5
    R6 = 6
    R7 = 7
    PC = 8
    COND = 9


_REGISTERS_COUNT = 10
_R = array.array('H', [0 for i in range(_REGISTERS_COUNT)])


def reg_write(which, value):
    _R[which.value] = value % _MEMORY_SIZE


def reg_read(which):
    return _R[which.value]
