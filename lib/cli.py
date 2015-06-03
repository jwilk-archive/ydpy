# encoding=UTF-8

# Copyright © 2007-2015 Jakub Wilk <jwilk@jwilk.net>
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

import argparse
import errno
import locale
import os.path
import sys
import re

from . import libydp
from . import format_color
from . import format_text

def read_config():
    data = {}
    try:
        with open('/etc/ydpdict.conf', 'rb') as file:
            for line in file:
                key, value = line.strip().split(None, 1)
                key = key.decode('ASCII')
                data[key] = value
    except IOError as ex:
        if ex.errno == errno.ENOENT:
            return {}
        raise
    return data

DICTIONARIES = \
(
    ('e', 'en-pl', 'English-Polish', 100),
    ('p', 'pl-en', 'Polish-English', 101),
    ('g', 'de-pl', 'German-Polish',  200),
    ('o', 'pl-de', 'Polish-German',  201),
)

config = read_config()

class ArgumentParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        argparse.ArgumentParser.__init__(self, *args, **kwargs)
        for short_name, long_name, text, value in DICTIONARIES:
            self.add_argument(
                '-%s' % short_name,
                '--%s' % long_name,
                action='store_const', const=value,
                dest='dict_n',
                help='use the %s dictionary' % text
            )
        self.add_argument('-f', '--path', action='store', help='dictionary data directory')
        self.add_argument('term', metavar='SEARCH-TERM', nargs='?')
        self.set_defaults(dict_n=100)

if str != unicode:
    # Python 2
    def write_bytes(file, bytestring):
        file.write(bytestring)
else:
    # Python 3
    def write_bytes(file, bytestring):
        file.flush()
        file.buffer.write(bytestring)

def main():
    options = ArgumentParser().parse_args()
    encoding = locale.getpreferredencoding()
    if options.term:
        term = options.term
        if not isinstance(term, unicode):
            term = term.decode(encoding)
        matcher = re.compile(term, re.UNICODE | re.IGNORECASE | re.DOTALL).search
    else:
        matcher = id
    path = options.path or config.get('Path') or '/usr/share/ydpdict'
    if isinstance(path, unicode):
        path = path.encode(sys.getfilesystemencoding())
    dict_n = options.dict_n
    if sys.stdout.isatty():
        YdpFormatter = format_color.YdpFormatter
    else:
        YdpFormatter = format_text.YdpFormatter
    formatter = None
    try:
        with libydp.YdpDict(os.path.join(path, ('dict%03d.dat' % dict_n).encode()), os.path.join(path, ('dict%03d.idx' % dict_n).encode())) as ydpd:
            for entry in ydpd:
                if not matcher(entry.name):
                    continue
                formatter = YdpFormatter(encoding=encoding)
                formatter(entry.definition)
                bytestring = formatter.encode()
                write_bytes(sys.stdout, bytestring)
    finally:
        if formatter:
            print formatter.cleanup()

# vim:ts=4 sw=4 et
