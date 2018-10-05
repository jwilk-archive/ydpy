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
color text formatter
'''

from . import colorterm
from . import format_text

class YdpFormatter(format_text.YdpFormatter):

    def set_color(self, value):
        old_value = self._color
        self._color = value
        self.write(colorterm.reset() + value, strip=False)
        return old_value

    def set_bold_color(self):
        return self.set_color(self._color + colorterm.bold())

    def cleanup(self):
        return colorterm.reset()

    def __init__(self, encoding):
        format_text.YdpFormatter.__init__(self, encoding)
        self._color = ''
        self._color_map = {
            'color: red;': colorterm.fgcolor(colorterm.RED),
            'color: green;': colorterm.fgcolor(colorterm.GREEN),
            'color: blue;': colorterm.fgcolor(colorterm.BLUE),
            'color: magenta;': colorterm.fgcolor(colorterm.MAGENTA),
        }

# vim:ts=4 sts=4 sw=4 et
