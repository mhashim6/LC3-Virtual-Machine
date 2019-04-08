def _getch_windows():
    ch = msvcrt.getch()
    return ch


def _getch_unix():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


try:
    import msvcrt
    getch = _getch_windows
except ImportError:
    import tty
    import termios
    import sys
    getch = _getch_unix
