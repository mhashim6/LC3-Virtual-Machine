from memory import mem_read, mem_write, Registers, reg_read, reg_write
from utils import sign_extend, ushort
from enum import Enum
from control_unit import Halt
from getc import getch
import sys


def _GETC():
    """get character from keyboard"""
    #we need to cast the comming char in 16-bit location
    return getch()
    


def _OUT():
    """output a character"""
    sys.stdout.write(chr(mem_read(reg_read(Registers.R0))))
    sys.stdout.flush()

def _PUTS():
    """output a word string"""
    i = reg_read(Registers.R0)
    ch = mem_read(i)
    while chr(ch) != '\0': #check if the char is not null then print this char
        sys.stdout.write(ch)
        i += 1
        ch = mem_read(i)
    sys.stdout.flush()  #equal to fflush() in c


def _IN():
    """input a string"""
    #get string from user
    ch_arr = list(map(ord, input()))
    #get memory location to write data in
    i = reg_read(Registers.R0)
    for ch in ch_arr:
        if chr(ch) != '\0':
            mem_write(ushort(i), ushort(ch))
            i += 1
        else:
            break
    
    """ch = _GETC()
    i = reg_read(Registers.R0)
    while chr(ch) != '\0':
        mem_write(i, ch)
        i += 1"""


def _PUTSP():
    """output a byte string"""
    for i in range(Registers.R0, (2**16)):
        c = mem_read(ushort(i))
        if chr(c) == '\0':
            break
        sys.stdout.write(chr(c & 0xFF))
        char = c >> 8
        if char:
            sys.stdout.write(chr(char))
    sys.stdout.flush()


def _HALT():
    """halt the program"""
    raise Halt()


class Traps(Enum):
    TRAP_GETC = 0x20    # get character from keyboard
    TRAP_OUT = 0x21     # output a character
    TRAP_PUTS = 0x22    # output a word string
    TRAP_IN = 0x23      # input a string
    TRAP_PUTSP = 0x24   # output a byte string
    TRAP_HALT = 0x25    # halt the program


_traps = {
    Traps.TRAP_GETC: _GETC,
    Traps.TRAP_OUT: _OUT,
    Traps.TRAP_PUTS: _PUTS,
    Traps.TRAP_IN: _IN,
    Traps.TRAP_PUTSP: _PUTSP,
    Traps.TRAP_HALT: _HALT
}


def trap_routine(code):
    return _traps[code]

