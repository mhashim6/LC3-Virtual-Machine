from control_unit import *
from memory import load_image
import array
import sys

PC_START = 0x3000


def read_Rom_file(name):
    rom = array.array('H', range(0))
    with open(name) as file:
        rom.frombytes(file.read())
        if sys.byteorder == 'little':
            rom.byteswap()
    return rom


def main():
    reg_write(Registers.PC, ushort(PC_START))
    rom = read_Rom_file()
    load_image(rom)

    try:
        while True:
            pc = reg_read(Registers.PC)
            instruction = mem_read(pc)
            execute(instruction)
    except Halt:  # TODO
        print('Halted.')


if __name__ == "__main__":
    main()
