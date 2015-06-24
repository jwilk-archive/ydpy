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
    u'\xa0': '\x20',
    u'°': '^o',
    u'·': '.',
    u'Ä': 'A',
    u'Ó': 'O',
    u'Ö': 'O',
    u'Ü': 'U',
    u'ß': 'ss',
    u'á': 'a',
    u'â': 'a',
    u'ä': 'a',
    u'æ': '<ae>',
    u'ç': 'c',
    u'é': 'e',
    u'ë': 'e',
    u'í': 'i',
    u'ï': 'i',
    u'ð': '<6>',
    u'ó': 'o',
    u'ô': 'o',
    u'ö': 'o',
    u'ü': 'u',
    u'ă': 'a',
    u'ą': 'a',
    u'Ć': 'C',
    u'ć': 'c',
    u'č': 'c',
    u'Ę': 'E',
    u'ę': 'e',
    u'Ł': 'L',
    u'ł': 'l',
    u'ń': 'n',
    u'ŋ': '<n>',
    u'ŕ': 'r',
    u'Ś': 'S',
    u'ś': 's',
    u'Ź': 'Z',
    u'ź': 'z',
    u'Ż': 'Z',
    u'ż': 'z',
    u'ɑ': '<a>',
    u'ɔ': '<o>',
    u'ə': '<e>',
    u'ɛ': '<E>',
    u'ɪ': '<i>',
    u'ʃ': '<|>',
    u'ʌ': '<^>',
    u'ʒ': '<3>',
    u'ˈ': "'",
    u'ː': ':',
    u'θ': '<0>',
    u'–': '--',
    u'‘': "`",
    u'’': "'",
    u'”': "''",
    u'„': ',,',
    u'†': '<t>',
    u'‡': '<tt>',
    u'…': '...',
}

def handler(exception):
    if isinstance(exception, (UnicodeEncodeError, UnicodeTranslateError)):
        s = u''.join(
            FALLBACK.get(ch, u'<?>')
            for ch in exception.object[exception.start:exception.end]
        )
        return s, exception.end
    else:
        raise TypeError(
            "Don't know how to handle {exc} in error callback".format(exc=exception.__class__.__name__)
        )

import codecs
codecs.register_error('transliterate', handler)
del codecs

# vim:ts=4 sts=4 sw=4 et
