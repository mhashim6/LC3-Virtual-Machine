from control_unit import execute
from traps import Halt
from memory import mem_read, mem_write, reg_read, reg_write, Registers, load_image
import array
import sys

PC_START = 0x3000


def read_Rom_file(name):
    with open(name, 'br') as image:
        load_image(image)


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 lc3.py [obj-file]')
        exit(2)

    reg_write(Registers.PC, PC_START)
    read_Rom_file(sys.argv[1])

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
