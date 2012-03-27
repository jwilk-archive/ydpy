#!/usr/bin/python
# encoding=UTF-8

# Copyright © 2010, 2012 Jakub Wilk <jwilk@jwilk.net>
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
*ydpy* is a command-line interface to the Collins English-Polish/Polish-English
and/or Langenscheidt German-Polish/Polish-German dictionaries distributed by
`Young Digital Planet`_.

.. _Young Digital Planet:
   http://ydp.com.pl/
'''

classifiers = '''
Development Status :: 4 - Beta
Environment :: Console
Intended Audience :: End Users/Desktop
License :: OSI Approved :: MIT License
Natural Language :: Polish
Operating System :: POSIX
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Topic :: Text Processing :: Linguistic
'''.strip().splitlines()

import distutils.core
import distutils.command.build_py

from lib import version

try:
    build_py = distutils.command.build_py.build_py_2to3
except AttributeError:
    build_py = distutils.command.build_py.build_py

distutils.core.setup(
    name = 'ydpy',
    version = version.__version__,
    license = 'MIT',
    description = 'command-line interface for Collins and Langenscheidt dictionaries',
    long_description = __doc__.strip(),
    classifiers = classifiers,
    url = 'http://jwilk.net/software/ydpy',
    author = 'Jakub Wilk',
    author_email = 'jwilk@jwilk.net',
    packages = ['ydpy'],
    package_dir = dict(ydpy='lib'),
    scripts = ['ydpy'],
    cmdclass = dict(build_py=build_py)
)

# vim:ts=4 sw=4 et
