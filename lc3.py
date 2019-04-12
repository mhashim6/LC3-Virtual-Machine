from control_unit import execute
from traps import Halt
from memory import mem_read, mem_write, reg_read, reg_write, Registers, load_image
import array
import sys

PC_START = 0x3000


def read_Rom_file(name):
    rom = array.array('H', range(0))
    with open(name, 'br') as file:
        rom.frombytes(file.read())
        if sys.byteorder == 'little':
            rom.byteswap()
    return rom


def main():
    reg_write(Registers.PC, PC_START)
    rom = read_Rom_file(input('Enter filename: '))
    load_image(rom)

    try:
        while True:
            pc = reg_read(Registers.PC)
            instruction = mem_read(pc)
            # increment PC by #1.
            reg_write(Registers.PC, reg_read(Registers.PC) + 1)
            execute(instruction)
    except Halt:  # TODO
        print('Halted.')


if __name__ == "__main__":
    main()
