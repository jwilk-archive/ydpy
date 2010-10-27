# encoding=UTF-8

# Copyright © 2007, 2008, 2009, 2010 Jakub Wilk <jwilk@jwilk.net>
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

try:
    curses.tparm('x'.encode())
except TypeError:
    # Python 3 bug. Let's work around it.
    def monkeypatch(original_tparm=curses.tparm):
        def tparm(arg, *args):
            arg = arg.decode()
            return original_tparm(arg, *args)
        curses.tparm = tparm
    monkeypatch()
    del monkeypatch

__sgr0 = curses.tigetstr('sgr0').decode('ASCII')

__bold = curses.tigetstr('bold').decode('ASCII')

__setaf = curses.tigetstr('setaf')
__setaf = [curses.tparm(__setaf, j).decode('ASCII') for j in range(8)]

__setab = curses.tigetstr('setab')
__setab = [curses.tparm(__setab, j).decode('ASCII') for j in range(8)]

# vim:ts=4 sw=4 et
