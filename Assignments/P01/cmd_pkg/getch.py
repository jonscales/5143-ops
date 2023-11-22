#!/usr/bin/env python
class Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):                 
        try:
            self.impl = _GetchWindows()     # try to create a Windows getch object
        except ImportError:
            self.impl = _GetchUnix()        # if that fails, create a Unix getch object

    def __call__(self): 
        return self.impl()                  # call the object's __call__ method


class _GetchUnix:
    def __init__(self):
        import tty, sys                     # import the tty and sys modules

    def __call__(self):
        import sys, tty, termios            # import the sys, tty, and termios modules
        fd = sys.stdin.fileno()             # get the file descriptor for stdin
        old_settings = termios.tcgetattr(fd) # save the old settings
        try:
            tty.setraw(sys.stdin.fileno())  # set the tty settings to raw mode
            ch = sys.stdin.read(1)          # read a character from stdin
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # restore the old settings
        return ch                           


class _GetchWindows:                        # Windows version of _GetchUnix
    def __init__(self):                     # import the msvcrt module
        import msvcrt

    def __call__(self):                     # call the msvcrt module's getch method
        import msvcrt                       
        return msvcrt.getch()               