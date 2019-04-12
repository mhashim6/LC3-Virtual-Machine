# import ctypes
import sys
import select

# _kbhit = ctypes.CDLL('./kbhit/kbhit.so')


def check_key():
    # select system call, unix only.
    _, w, _ = select.select([], [sys.stdin], [], 0)
    return len(w)
