import ctypes


_kbhit = ctypes.CDLL('./kbhit/kbhit.so')


def check_key():
    return _kbhit.check_key()
