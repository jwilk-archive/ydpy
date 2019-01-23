# Copyright © 2019 Jakub Wilk <jwilk@jwilk.net>
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

import io
import os
import signal
import unittest.mock

from nose.tools import (
    assert_equal,
)

import lib.cli

def TextIO():
    fp = io.BytesIO()
    return io.TextIOWrapper(fp, encoding='UTF-8')

def get_io_string(fp):
    fp.flush()
    s = fp.buffer.getvalue()
    s = s.decode(fp.encoding)
    return s

def test_cli():
    here = os.path.dirname(__file__)
    signal_mock = unittest.mock.Mock()
    stdout_mock = TextIO()
    stderr_mock = TextIO()
    with unittest.mock.patch('signal.signal', signal_mock):
        with unittest.mock.patch('sys.argv', ['ydpy', '-f', here]):
            with unittest.mock.patch('sys.stdout', stdout_mock):
                with unittest.mock.patch('sys.stderr', stderr_mock):
                    lib.cli.main()
    signal_mock.assert_called_with(signal.SIGPIPE, signal.SIG_DFL)
    stdout = get_io_string(stdout_mock)
    stderr = get_io_string(stderr_mock)
    assert_equal(
        stdout,
        'słowo [wymowa]\n'
        'część mowy\n'
        ' (dziedzina)definicja,definicja rodzaj\n\n'
        '  Przykład użycia.\n\n\n'
    )
    assert_equal(stderr, '')

# vim:ts=4 sts=4 sw=4 et
