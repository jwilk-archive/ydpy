# encoding=UTF-8

# Copyright © 2007-2016 Jakub Wilk <jwilk@jwilk.net>
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

import collections
from StringIO import StringIO

from . import transliterate
del transliterate  # Hi, pyflakes!

class YdpFormatter(object):

    class UnhandledTag(Exception):
        pass

    def parse_body(self, node):
        for subnode in node:
            self(subnode)
        self.write('\n\n')

    def parse_p(self, node):
        self._strip = True
        self.write(node.text)
        for subnode in node:
            self(subnode)
        self.write('\n')
        self.write(node.tail)

    def parse_a(self, node):
        self.write(node.text)
        for subnode in node:
            self(subnode)
        self.write(node.tail)

    def parse_b(self, node):
        tmp_color = self.set_bold_color()
        self.write(node.text)
        for subnode in node:
            self(subnode)
        self.set_color(tmp_color)
        self.write(node.tail)

    def parse_i(self, node):
        self.write(node.text)
        for subnode in node:
            self(subnode)
        self.write(node.tail)

    def parse_sup(self, node):
        self.write('^')
        self.write(node.text)
        for subnode in node:
            self(subnode)
        self.write(node.tail)

    def parse_div(self, node):
        tmp_file = self._file
        self._file = StringIO()
        for subnode in node:
            self(subnode)
        result = unicode(self)
        self._file = tmp_file
        self.write('\n  ')
        self.write(result.replace('\n', '\n  '))
        self.write('\n\n')
        self._strip = True

    def parse_span(self, node):
        style = node.get('style')
        color = self._color_map[style]
        tmp_color = self.set_color(color)
        self.write(node.text)
        for subnode in node:
            self(subnode)
        self.set_color(tmp_color)
        self.write(node.tail)

    def parse_br(self, node):
        self.write('\n')
        self.write(node.tail)
        self._strip = True

    def write(self, value, strip=True):
        value = value or ''
        if self._strip and strip:
            if value:
                value = value.lstrip()
                self._strip = False
        self._file.write(value)

    def set_color(self, value):
        pass

    def set_bold_color(self):
        pass

    def cleanup(self):
        return ''.encode()

    def __init__(self, encoding):
        self._file = StringIO()
        self._strip = False
        self._color_map = collections.defaultdict(str)
        self._encoding = encoding

    if str is bytes:
        # Python 2
        def __unicode__(self):
            return self._file.getvalue()
        def __str__(self):
            return unicode(self).encode(self._encoding, 'transliterate')
        def encode(self):
            return str(self)
    else:
        # Python 3
        def __str__(self):
            return self._file.getvalue()
        def encode(self):
            return str(self).encode(self._encoding, 'transliterate')

    def __call__(self, node):
        if node.tag.isalpha():
            try:
                getattr(self, 'parse_{tag}'.format(tag=node.tag))(node)
                return
            except AttributeError:
                pass
        raise YdpFormatter.UnhandledTag(node.tag)

# vim:ts=4 sts=4 sw=4 et
