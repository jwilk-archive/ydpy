from curses import setupterm, tigetstr, tparm

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

setupterm()

__sgr0 = tigetstr('sgr0')

__bold = tigetstr('bold')

__setaf = tigetstr('setaf')
__setaf = [tparm(__setaf, j) for j in range(8)]

__setab = tigetstr('setab')
__setab = [tparm(__setab, j) for j in range(8)]

# vim:ts=4 sw=4 et
