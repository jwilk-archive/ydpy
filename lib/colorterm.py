# encoding=UTF-8

# Copyright © 2007-2018 Jakub Wilk <jwilk@jwilk.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
color terminal support
'''

import curses
import functools
import os
import re

_setaf = []
_setab = []
_bold = []
_sgr0 = []

def fgcolor(i):
    return _setaf[i]

def bgcolor(i):
    return _setab[i]

def bold():
    return _bold[0]

def reset():
    return _sgr0[0]

BLACK = 0
RED = 1
GREEN = 2
YELLOW = 3
BLUE = 4
MAGENTA = 5
CYAN = 6
WHITE = 7

_empty_bytes = b''

_strip_delay = functools.partial(
    re.compile(b'[$]<([0-9]*[.])?[0-9]+([/*]|[*][/])?>').sub,
    _empty_bytes
)

def init():
    try:
        curses.setupterm()
    except curses.error:
        os.putenv('TERM', 'dumb')
        curses.setupterm()
    c_sgr0 = curses.tigetstr('sgr0') or _empty_bytes
    c_sgr0 = _strip_delay(c_sgr0).decode()
    _sgr0[:] = [c_sgr0]
    c_bold = curses.tigetstr('bold') or _empty_bytes
    c_bold = _strip_delay(c_bold).decode()
    _bold[:] = [c_bold]
    curses.tparm(b'x')  # work-around for https://bugs.debian.org/902630
    c_setaf = curses.tigetstr('setaf') or _empty_bytes
    c_setaf = _strip_delay(c_setaf)
    _setaf[:] = [curses.tparm(c_setaf, j).decode() for j in range(8)]
    c_setab = curses.tigetstr('setab') or _empty_bytes
    c_setab = _strip_delay(c_setab)
    _setab[:] = [curses.tparm(c_setab, j).decode() for j in range(8)]

# vim:ts=4 sts=4 sw=4 et
