from memory import mem_read, mem_write, Registers, reg_read, reg_write
from utils import sign_extend
from getch import getch
import sys


class Halt(Exception):
    """Thrown to indicate HALT instruction has been executed."""
    pass


def _GETC():
    """get character from keyboard,
     character is not echoed onto the console. """
    ch = getch()
    reg_write(Registers.R0, ord(ch))


def _OUT():
    """output a character"""
    sys.stdout.write(chr(reg_read(Registers.R0)))
    sys.stdout.flush()


def _PUTS():
    """output a word string"""
    for i in range(reg_read(Registers.R0), 2**16):
        ch = mem_read(i)
        if ch == 0:  # check if the char is not null then print this char
            break
        sys.stdout.write(chr(ch))
    sys.stdout.flush()  # equal to fflush() in c


def _IN():
    """input a single character, echoed onto the console"""
    sys.stdout.write("Enter a character: ")
    sys.stdout.flush()
    reg_write(Registers.R0, ord(sys.stdin.read(1)))


def _PUTSP():
    """output a byte string"""
    for i in range(reg_read(Registers.R0), 2**16):
        c = mem_read(i)
        if c == 0:
            break
        sys.stdout.write(chr(c & 0xFF))
        char = c >> 8
        if char:
            sys.stdout.write(chr(char))
    sys.stdout.flush()


def _HALT():
    """halt the program"""
    raise Halt()


class Traps:
    GETC = 0x20    # get character from keyboard
    OUT = 0x21     # output a character
    PUTS = 0x22    # output a word string
    IN = 0x23      # input a string
    PUTSP = 0x24   # output a byte string
    HALT = 0x25    # halt the program


_traps = {
    Traps.GETC: _GETC,
    Traps.OUT: _OUT,
    Traps.PUTS: _PUTS,
    Traps.IN: _IN,
    Traps.PUTSP: _PUTSP,
    Traps.HALT: _HALT
}


def trap_routine(code):
    return _traps[code]
