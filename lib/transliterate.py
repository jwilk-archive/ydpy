# encoding=UTF-8

# Copyright © 2007-2010 Jakub Wilk <jwilk@jwilk.net>
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

FALLBACK = {
    '\xa0': '\x20',
    '°': '^o',
    '·': '.',
    'Ä': 'A',
    'Ó': 'O',
    'Ö': 'O',
    'Ü': 'U',
    'ß': 'ss',
    'á': 'a',
    'â': 'a',
    'ä': 'a',
    'æ': '<ae>',
    'ç': 'c',
    'é': 'e',
    'ë': 'e',
    'í': 'i',
    'ï': 'i',
    'ð': '<6>',
    'ó': 'o',
    'ô': 'o',
    'ö': 'o',
    'ü': 'u',
    'ă': 'a',
    'ą': 'a',
    'Ć': 'C',
    'ć': 'c',
    'č': 'c',
    'Ę': 'E',
    'ę': 'e',
    'Ł': 'L',
    'ł': 'l',
    'ń': 'n',
    'ŋ': '<n>',
    'ŕ': 'r',
    'Ś': 'S',
    'ś': 's',
    'Ź': 'Z',
    'ź': 'z',
    'Ż': 'Z',
    'ż': 'z',
    'ɑ': '<a>',
    'ɔ': '<o>',
    'ə': '<e>',
    'ɛ': '<E>',
    'ɪ': '<i>',
    'ʃ': '<|>',
    'ʌ': '<^>',
    'ʒ': '<3>',
    'ˈ': "'",
    'ː': ':',
    'θ': '<0>',
    '–': '--',
    '‘': "`",
    '’': "'",
    '”': "''",
    '„': ',,',
    '†': '<t>',
    '‡': '<tt>',
    '…': '...',
}

def handler(exception):
    if isinstance(exception, (UnicodeEncodeError, UnicodeTranslateError)):
        s = ''.join(
            FALLBACK.get(ch, '<?>')
            for ch in exception.object[exception.start:exception.end]
        )
        return s, exception.end
    else:
        raise TypeError(
            "Don't know how to handle {exc} in error callback".format(exc=type(exception).__name__)
        )

import codecs
codecs.register_error('transliterate', handler)
del codecs

# vim:ts=4 sts=4 sw=4 et
