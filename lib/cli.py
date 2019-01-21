# encoding=UTF-8

# Copyright © 2007-2019 Jakub Wilk <jwilk@jwilk.net>
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
ydpy CLI
'''

import argparse
import locale
import os.path
import sys
import re

from . import libydp
from . import format_color
from . import format_text
from . import version

def read_config():
    data = {}
    try:
        with open('/etc/ydpdict.conf', 'rb') as file:
            for line in file:
                key, value = line.strip().split(None, 1)
                key = key.decode('ASCII')
                data[key] = value
    except FileNotFoundError:
        return {}
    return data

DICTIONARIES = (
    ('e', 'en-pl', 'English-Polish', 100),
    ('p', 'pl-en', 'Polish-English', 101),
    ('g', 'de-pl', 'German-Polish', 200),
    ('o', 'pl-de', 'Polish-German', 201),
)

class VersionAction(argparse.Action):
    '''
    argparse --version action
    '''

    def __init__(self, option_strings, dest=argparse.SUPPRESS):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            help='show version information and exit'
        )

    def __call__(self, parser, namespace, values, option_string=None):
        print('{prog} {0}'.format(version.__version__, prog=parser.prog))
        print('+ Python {0}.{1}.{2}'.format(*sys.version_info))
        print('+ lxml {0}'.format(libydp.lxml.etree.__version__))
        parser.exit()

class ArgumentParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        argparse.ArgumentParser.__init__(self, *args, **kwargs)
        self.add_argument('--version', action=VersionAction)
        for short_name, long_name, name, value in DICTIONARIES:
            self.add_argument(
                '-{c}'.format(c=short_name),
                '--{opt}'.format(opt=long_name),
                action='store_const', const=value,
                dest='dict_n',
                help='use the {name} dictionary'.format(name=name),
            )
        self.add_argument('-f', '--path', action='store', help='dictionary data directory')
        self.add_argument('term', metavar='REGEXP', nargs='?')
        self.set_defaults(dict_n=100)

def main():
    ap = ArgumentParser()
    options = ap.parse_args()
    encoding = locale.getpreferredencoding()
    if options.term:
        term = options.term
        matcher = re.compile(term, re.IGNORECASE | re.DOTALL).search
    else:
        matcher = id
    try:
        config = read_config()
    except OSError as exc:
        print('{prog}: error: {path}: {exc}'.format(
            prog=ap.prog, path=exc.filename, exc=exc.strerror
        ))
        sys.exit(1)
    path = options.path or config.get('Path') or '/usr/share/ydpdict'
    if isinstance(path, str):
        path = os.fsencode(path)
    dict_n = options.dict_n
    if sys.stdout.isatty():
        YdpFormatter = format_color.YdpFormatter
    else:
        YdpFormatter = format_text.YdpFormatter
    formatter = None
    try:
        paths = [
            os.path.join(path, 'dict{n:03}.{ext}'.format(n=dict_n, ext=ext).encode())
            for ext in ['dat', 'idx']
        ]
        try:
            ydpd = libydp.YdpDict(*paths)
        except OSError as exc:
            print('{prog}: error: {path}: {exc}'.format(
                prog=ap.prog, path=exc.filename, exc=exc.strerror
            ))
            sys.exit(1)
        with ydpd:
            for entry in ydpd:
                if not matcher(entry.name):
                    continue
                formatter = YdpFormatter(encoding=encoding)
                formatter(entry.definition)
                bytestring = formatter.encode()
                sys.stdout.flush()
                sys.stdout.buffer.write(bytestring)
    finally:
        if formatter:
            print(formatter.cleanup())

# vim:ts=4 sts=4 sw=4 et
