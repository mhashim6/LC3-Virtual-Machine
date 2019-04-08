from utils import ushort

def getch_windows():
    import msvcrt
    ch = msvcrt.getch()
    return ushort(ord(ch))

def getch_unix():
    import tty, termios, sys
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        #don't know if this gonna work
    return ushort(ord(ch))

def getch():
    try: #for windows
        getch_windows()
    except ImportError:
        #for linux
        getch_unix()