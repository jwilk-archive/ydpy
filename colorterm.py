import curses

def fgcolor(i):
    return __setaf[i]

def bgcolor(i):
    return __setab[i]

def bold():
    return __bold

def reset():
    return __sgr0

BLACK = 0
RED = 1
GREEN = 2
YELLOW = 3
BLUE = 4
MAGENTA = 5
CYAN = 6
WHITE = 7

curses.setupterm()

__sgr0 = curses.tigetstr('sgr0')

__bold = curses.tigetstr('bold')

__setaf = curses.tigetstr('setaf')
__setaf = [curses.tparm(__setaf, j) for j in range(8)]

__setab = curses.tigetstr('setab')
__setab = [curses.tparm(__setab, j) for j in range(8)]

# vim:ts=4 sw=4 et
