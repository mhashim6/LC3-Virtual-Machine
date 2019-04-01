from memory import mem_read, mem_write, Registers, reg_read, reg_write
from utils import sign_extend, wordOf
from enum import Enum


def _GETC():
    """get character from keyboard"""
    pass


def _OUT():
    """output a character"""
    pass


def _PUTS():
    """output a word string"""
    pass


def _IN():
    """input a string"""
    pass


def _PUTSP():
    """output a byte string"""
    pass


def _HALT():
    """halt the program"""
    pass


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
