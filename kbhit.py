import ctypes


_kbhit = ctypes.CDLL('./kbhit/kbhit.so')
_kbhit.setup()


def check_key():
    return _kbhit.check_key()


def kbhit_terminate():
    _kbhit.terminate()
